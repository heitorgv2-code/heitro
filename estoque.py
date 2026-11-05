#!/usr/bin/env python3
"""Estoque de calçados (SQLite). Uso:
  python3 estoque.py add CODIGO "modelo" "marca" "cor" TAMANHO QTD ["obs"]
  python3 estoque.py foto CODIGO calcado|folha fotos/arquivo.jpg
  python3 estoque.py list
"""
import sqlite3, sys

DB = "estoque.db"

def conectar():
    con = sqlite3.connect(DB)
    con.execute("""CREATE TABLE IF NOT EXISTS calcados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT NOT NULL,
        modelo TEXT NOT NULL,
        marca TEXT,
        cor TEXT,
        tamanho_br INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        observacao TEXT,
        UNIQUE (codigo, tamanho_br)
    )""")
    con.execute("""CREATE TABLE IF NOT EXISTS fotos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT NOT NULL,
        tipo TEXT NOT NULL,
        arquivo TEXT NOT NULL,
        UNIQUE (codigo, tipo)
    )""")
    cols = [r[1] for r in con.execute("PRAGMA table_info(calcados)")]
    for c in ("preco", "preco_promo"):
        if c not in cols:
            con.execute(f"ALTER TABLE calcados ADD COLUMN {c} REAL")
    return con

def main():
    con = conectar()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "add":
        codigo, modelo, marca, cor, tam, qtd = sys.argv[2:8]
        obs = sys.argv[8] if len(sys.argv) > 8 else None
        preco = float(sys.argv[9]) if len(sys.argv) > 9 else None
        promo = float(sys.argv[10]) if len(sys.argv) > 10 else None
        con.execute("""INSERT INTO calcados (codigo, modelo, marca, cor, tamanho_br, quantidade, observacao, preco, preco_promo)
            VALUES (?,?,?,?,?,?,?,?,?)
            ON CONFLICT(codigo, tamanho_br) DO UPDATE SET quantidade=excluded.quantidade,
              modelo=excluded.modelo, marca=excluded.marca, cor=excluded.cor, observacao=excluded.observacao,
              preco=excluded.preco, preco_promo=excluded.preco_promo""",
            (codigo, modelo, marca, cor, int(tam), int(qtd), obs, preco, promo))
        con.commit()
    if cmd == "foto":  # foto CODIGO TIPO(calcado|folha) ARQUIVO
        codigo, tipo, arquivo = sys.argv[2:5]
        con.execute("""INSERT INTO fotos (codigo, tipo, arquivo) VALUES (?,?,?)
            ON CONFLICT(codigo, tipo) DO UPDATE SET arquivo=excluded.arquivo""", (codigo, tipo, arquivo))
        con.commit()
    for r in con.execute("SELECT codigo, modelo, marca, cor, tamanho_br, quantidade, preco, preco_promo, observacao FROM calcados ORDER BY codigo, tamanho_br"):
        print(r)

main()

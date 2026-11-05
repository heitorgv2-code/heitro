#!/usr/bin/env python3
"""Estoque de calçados (SQLite). Uso:
  python3 estoque.py add CODIGO "modelo" "marca" "cor" TAMANHO QTD ["obs"]
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
    return con

def main():
    con = conectar()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "add":
        codigo, modelo, marca, cor, tam, qtd = sys.argv[2:8]
        obs = sys.argv[8] if len(sys.argv) > 8 else None
        con.execute("""INSERT INTO calcados (codigo, modelo, marca, cor, tamanho_br, quantidade, observacao)
            VALUES (?,?,?,?,?,?,?)
            ON CONFLICT(codigo, tamanho_br) DO UPDATE SET quantidade=excluded.quantidade,
              modelo=excluded.modelo, marca=excluded.marca, cor=excluded.cor, observacao=excluded.observacao""",
            (codigo, modelo, marca, cor, int(tam), int(qtd), obs))
        con.commit()
    for r in con.execute("SELECT codigo, modelo, marca, cor, tamanho_br, quantidade, observacao FROM calcados ORDER BY codigo, tamanho_br"):
        print(r)

main()

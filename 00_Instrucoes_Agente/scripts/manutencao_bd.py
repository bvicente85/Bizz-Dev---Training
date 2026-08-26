import os
import shutil
import argparse
from pathlib import Path

# Configurações de pastas
BASE_DIR = Path(r"C:\Users\brunn\OneDrive - GIE IFE\Desktop\Bruno\PESSOAL\Business Development Formação\03_Carteira_Clientes")
CLIENTES_DIR = BASE_DIR / "032_Clientes"
ARQUIVO_DIR = BASE_DIR / "032_Clientes_Arquivo"

# Limites
MAX_LINES_NOTES = 20

def run_maintenance(dry_run=True):
    print(f"=== SKOLAE BD Manutenção Automática ===")
    print(f"Modo: {'DRY-RUN (Simulação)' if dry_run else 'EXECUÇÃO (Alteração de Dados)'}\n")
    
    if not CLIENTES_DIR.exists():
        print("Pasta de clientes não encontrada.")
        return

    # Passo 1: Arquivar clientes inativos
    clientes_para_arquivar = []
    
    for client_dir in CLIENTES_DIR.iterdir():
        if client_dir.is_dir():
            progress_file = client_dir / f"{client_dir.name}_progress.md"
            if progress_file.exists():
                with open(progress_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read().lower()
                    if "fechada/perdida" in content or "fechado/perdido" in content or "inativo" in content:
                        clientes_para_arquivar.append(client_dir)

    print("--- 1. Clientes a Arquivar (Inativos/Perdidos) ---")
    if not clientes_para_arquivar:
        print("Nenhum cliente inativo encontrado.")
    
    for c in clientes_para_arquivar:
        dest = ARQUIVO_DIR / c.name
        print(f"[ARQUIVAR] {c.name} -> {dest}")
        if not dry_run:
            if not ARQUIVO_DIR.exists():
                ARQUIVO_DIR.mkdir(parents=True, exist_ok=True)
            shutil.move(str(c), str(dest))
            print("   -> Movido com sucesso.")

    print("\n--- 2. Notas de Reunião a Resumir (Token Optimization) ---")
    # Passo 2: Otimização de Memória (Identificar ficheiros grandes)
    for client_dir in CLIENTES_DIR.iterdir():
        if client_dir.is_dir():
            notes_file = client_dir / f"{client_dir.name}_meeting_notes.md"
            if notes_file.exists():
                with open(notes_file, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    if len(lines) > MAX_LINES_NOTES:
                        print(f"[AVISO] {client_dir.name} tem notas com {len(lines)} linhas. Requer sumarização pela LLM.")

    print("\nConcluído.")
    if dry_run:
        print("\nPara executar as movimentações, corra o script com a flag --execute")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script de manutenção de BD de clientes")
    parser.add_argument("--execute", action="store_true", help="Executa as alterações de ficheiros (desativa o dry-run)")
    args = parser.parse_args()
    
    run_maintenance(dry_run=not args.execute)

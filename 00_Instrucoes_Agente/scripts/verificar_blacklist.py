import json
import sys
import os

def check_email(email):
    # Adjust path relative to script location
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    blacklist_path = os.path.join(base_dir, '01_Conhecimento_Base', 'blacklist.json')
    
    if not os.path.exists(blacklist_path):
        print(f"[ERRO] Ficheiro blacklist.json não encontrado em {blacklist_path}")
        return
        
    with open(blacklist_path, 'r', encoding='utf-8') as f:
        blacklist = set([e.lower().strip() for e in json.load(f)])
        
    email_clean = email.lower().strip()
    if email_clean in blacklist:
        print(f"[BLOQUEIO] O email {email} está na BLACKLIST. É ESTRITAMENTE PROIBIDO gerar texto ou enviar propostas para este contacto.")
        sys.exit(1)
    else:
        print(f"[OK] O email {email} não está na blacklist. Pode prosseguir.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python verificar_blacklist.py <email>")
        sys.exit(1)
    check_email(sys.argv[1])

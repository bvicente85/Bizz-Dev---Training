import sys

def calcular_margem(preco_venda, custos_diretos):
    if preco_venda <= 0:
        print("[ERRO] O preço de venda deve ser maior que zero.")
        sys.exit(1)
        
    margem_absoluta = preco_venda - custos_diretos
    margem_percentual = (margem_absoluta / preco_venda) * 100
    
    print(f"Preço de Venda: {preco_venda:.2f} €")
    print(f"Custos Diretos: {custos_diretos:.2f} €")
    print(f"Margem Bruta Absoluta: {margem_absoluta:.2f} €")
    print(f"Margem Bruta %: {margem_percentual:.2f}%")
    
    if margem_percentual < 65.0:
        print("\n[ALERTA CRÍTICO] A margem bruta é inferior a 65%. PROPOSTA SUB-OTIMIZADA.")
        print("É estritamente proibido avançar com esta proposta sem alertar o Bruno e obter autorização expressa para a exceção.")
        sys.exit(1)
    else:
        print("\n[OK] Margem aprovada (>= 65%). Pode prosseguir com a redação da proposta.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python calcular_margem.py <preco_venda> <custos_diretos>")
        sys.exit(1)
        
    try:
        preco_venda = float(sys.argv[1])
        custos_diretos = float(sys.argv[2])
    except ValueError:
        print("[ERRO] Os valores devem ser números válidos.")
        sys.exit(1)
        
    calcular_margem(preco_venda, custos_diretos)

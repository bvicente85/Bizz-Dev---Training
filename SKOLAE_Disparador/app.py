from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

EXCEL_PATH = r"\\?\c:\Users\brunn\OneDrive - GIE IFE\Desktop\Bruno\PESSOAL\Business Development Formação\03_Carteira_Clientes\031_Bases_Dados\Contacts 2026-2027.xlsx"
LOG_PATH = r"\\?\c:\Users\brunn\OneDrive - GIE IFE\Desktop\Bruno\PESSOAL\Business Development Formação\03_Carteira_Clientes\031_Bases_Dados\Historico_Envios.xlsx"

REST_DAYS = 15

def read_excel():
    df = pd.read_excel(EXCEL_PATH)
    df = df.fillna('')
    df['id'] = df.index
    return df

def write_excel(df):
    df.drop(columns=['id'], errors='ignore', inplace=True)
    df.to_excel(EXCEL_PATH, index=False)

def read_log():
    normal_path = LOG_PATH.replace('\\\\?\\', '')
    if not os.path.exists(normal_path):
        return pd.DataFrame(columns=['Data', 'Tema', 'ContactID', 'Nome', 'Email', 'Empresa'])
    
    # LER TODAS AS FOLHAS (SHEETS)
    all_sheets = pd.read_excel(LOG_PATH, sheet_name=None)
    if not all_sheets:
        return pd.DataFrame(columns=['Data', 'Tema', 'ContactID', 'Nome', 'Email', 'Empresa'])
        
    # Juntar todas as folhas num unico DataFrame para o Dashboard e Estatisticas
    df = pd.concat(all_sheets.values(), ignore_index=True)
    return df

def write_log(new_df, month_sheet_name):
    normal_path = LOG_PATH.replace('\\\\?\\', '')
    
    if not os.path.exists(normal_path):
        all_sheets = {}
    else:
        all_sheets = pd.read_excel(LOG_PATH, sheet_name=None)
    
    # Adicionar os novos dados à folha do mês correspondente
    if month_sheet_name in all_sheets:
        all_sheets[month_sheet_name] = pd.concat([all_sheets[month_sheet_name], new_df], ignore_index=True)
    else:
        all_sheets[month_sheet_name] = new_df
        
    # Gravar o ficheiro com todas as folhas
    with pd.ExcelWriter(LOG_PATH, engine='openpyxl') as writer:
        for sheet_name, df in all_sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/campaigns/eligible', methods=['GET'])
def get_eligible_contacts():
    try:
        df = read_excel()
        today = datetime.now()
        category_filter = request.args.get('category', '').strip()
        
        available_categories = []
        if 'Category' in df.columns:
            available_categories = [str(c).strip() for c in df['Category'].dropna().unique() if str(c).strip()]
            
        eligible_contacts = []
        for _, row in df.iterrows():
            if category_filter and category_filter != 'Todas as Contas':
                if str(row.get('Category', '')).strip() != category_filter:
                    continue
                    
            last_sent_str = str(row.get('Data Ultimo Envio', '')).strip()
            email = str(row.get('Email', '')).strip()
            
            if not email or '@' not in email:
                continue

            is_eligible = False
            if not last_sent_str:
                is_eligible = True
            else:
                try:
                    last_sent_date = datetime.strptime(last_sent_str[:10], '%Y-%m-%d')
                    if (today - last_sent_date).days >= REST_DAYS:
                        is_eligible = True
                except Exception:
                    is_eligible = True
            
            if is_eligible:
                eligible_contacts.append({
                    'id': row['id'],
                    'Name': row.get('Name', ''),
                    'Company': row.get('Company', ''),
                    'Email': email
                })

        batch_size = 50
        batches = [eligible_contacts[i:i + batch_size] for i in range(0, len(eligible_contacts), batch_size)]
        
        log_df = read_log()
        past_themes = list(log_df['Tema'].unique()) if not log_df.empty else []
        past_themes = [t for t in past_themes if str(t).strip()]
        
        return jsonify({
            'total_eligible': len(eligible_contacts),
            'rest_days': REST_DAYS,
            'batches': batches,
            'past_themes': past_themes,
            'available_categories': available_categories
        })
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/campaigns/mark_sent', methods=['POST'])
def mark_sent():
    data = request.json
    contact_ids = data.get('contact_ids', [])
    tema = data.get('tema', 'Sem Tema')
    
    if not contact_ids:
        return jsonify({'error': 'No ids provided'}), 400
        
    df = read_excel()
    today_str = datetime.now().strftime('%Y-%m-%d')
    month_str = today_str[:7] # YYYY-MM (Ex: 2026-08)
    
    new_logs = []
    
    for cid in contact_ids:
        if cid < len(df):
            df.at[cid, 'Data Ultimo Envio'] = today_str
            new_logs.append({
                'Data': today_str,
                'Tema': tema,
                'ContactID': cid,
                'Nome': df.at[cid, 'Name'],
                'Email': df.at[cid, 'Email'],
                'Empresa': df.at[cid, 'Company'],
                'Funcao': str(df.at[cid, 'Role']).strip() if str(df.at[cid, 'Role']).strip() else 'Desconhecido',
                'AccountType': str(df.at[cid, 'Category']).strip() if str(df.at[cid, 'Category']).strip() else 'Desconhecido'
            })
            
    if new_logs:
        new_df = pd.DataFrame(new_logs)
        write_log(new_df, month_str)
        
    write_excel(df)
    return jsonify({'message': 'Success', 'marked': len(contact_ids)})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        log_df = read_log()
        if log_df.empty:
            return jsonify({'themes': {}, 'roles': {}, 'categories': {}, 'timeline': {}, 'recent_history': []})
            
        theme_counts = log_df['Tema'].value_counts().to_dict()
        role_counts = log_df['Funcao'].value_counts().to_dict() if 'Funcao' in log_df.columns else {}
        category_counts = log_df['AccountType'].value_counts().to_dict() if 'AccountType' in log_df.columns else {}
        log_df['Data'] = log_df['Data'].astype(str).str[:10]
        timeline_counts = log_df.groupby('Data').size().to_dict()
        
        history_table = log_df.iloc[::-1].fillna('').to_dict(orient='records')
        
        return jsonify({
            'themes': theme_counts,
            'roles': role_counts,
            'categories': category_counts,
            'timeline': timeline_counts,
            'recent_history': history_table
        })
    except Exception as e:
        print(e)
        return jsonify({'themes': {}, 'roles': {}, 'categories': {}, 'timeline': {}, 'recent_history': []})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

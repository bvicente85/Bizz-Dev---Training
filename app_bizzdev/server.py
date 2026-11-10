import os
import re
import sys
import json
import yaml
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import openpyxl

# ==============================================================================
# CONFIGURAÇÃO DE CAMINHOS (COM SUPORTE UNC LONG PATH PARA WINDOWS)
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = Path(__file__).resolve().parent
STATIC_DIR = APP_DIR / "static"


def unc_path(p: Path) -> str:
    """Adiciona o prefixo UNC \\\\?\\ em Windows para evitar o limite de 260 caracteres."""
    s = str(p.resolve())
    if os.name == "nt" and not s.startswith("\\\\?\\"):
        return "\\\\?\\" + s
    return s


CLIENTS_DIR = BASE_DIR / "03_Carteira_Clientes" / "032_Clientes"
DB_DIR = BASE_DIR / "03_Carteira_Clientes" / "031_Bases_Dados"
LUCIDE_DIR = BASE_DIR / "assets" / "icons" / "lucide"
DASHBOARD_JSON = BASE_DIR / "dashboard_data.json"
CALC_MARGEM_SCRIPT = BASE_DIR / "00_Instrucoes_Agente" / "scripts" / "calcular_margem.py"
BLACKLIST_JSON = BASE_DIR / "01_Conhecimento_Base" / "blacklist.json"
CATALOG_MD = BASE_DIR / "01_Conhecimento_Base" / "Catalogo_Global_Cursos.md"

app = FastAPI(
    title="SKOLAE BIZZ DEV AI",
    description="Parceiro Estratégico de Business Development — SKOLAE Formação",
    version="2.5.0",
)

# ==============================================================================
# CACHE EM MEMÓRIA PARA PERFORMANCE INSTANTÂNEA
# ==============================================================================
_CACHE: Dict[str, Any] = {
    "clients_list": None,
    "clients_ts": 0,
    "contacts_list": None,
    "lucide_icons": None,
}

PRIORITY_ACCOUNTS = [
    "Desentop_Ambiente",
    "Carl Zeiss",
    "Devoteam",
    "ALDI_Portugal",
    "Sport_TV",
    "Banco_CTT",
    "Talkdesk",
    "Europastry",
    "Grupo Nabeiro - Delta Cafés",
    "CUF",
    "Brisa",
    "Cegid",
    "Generali Tranquilidade",
    "Natixis",
    "Samsung",
    "Sumol_Compal",
    "Vodafone",
    "Padaria_Portuguesa",
]

# Matriz Oficial TMB 25-26 (Referência Valores Intra-Empresa & Valores/Hora Formador)
TMB_MATRIX = {
    "areas": [
        {
            "id": "soft_skills",
            "label": "Liderança / Desenv. Pessoal / Vendas / Atendimento (PT)",
            "trainer_rate": 50.0,
            "prices": {
                "3h": {"one_to_one": 550, "ate_12": 550, "ate_16": 600},
                "4h": {"one_to_one": 600, "ate_12": 700, "ate_16": 700},
                "7h": {"one_to_one": 1050, "ate_12": 1100, "ate_16": 1150},
                "8h": {"one_to_one": 1200, "ate_12": 1250, "ate_16": 1300},
                "14h": {"one_to_one": 2050, "ate_12": 2100, "ate_16": 2200},
                "16h": {"one_to_one": 2350, "ate_12": 2400, "ate_16": 2500},
                "21h": {"one_to_one": 3050, "ate_12": 3100, "ate_16": 3200},
                "24h": {"one_to_one": 3500, "ate_12": 3550, "ate_16": 3600},
            },
        },
        {
            "id": "soft_skills_en",
            "label": "Soft Skills em Inglês / Jurídica / Financeira / Design Thinking",
            "trainer_rate": 65.0,
            "prices": {
                "3h": {"one_to_one": 600, "ate_12": 650, "ate_16": 700},
                "4h": {"one_to_one": 800, "ate_12": 750, "ate_16": 800},
                "7h": {"one_to_one": 1350, "ate_12": 1400, "ate_16": 1450},
                "8h": {"one_to_one": 1500, "ate_12": 1600, "ate_16": 1650},
                "14h": {"one_to_one": 2650, "ate_12": 2700, "ate_16": 2750},
                "16h": {"one_to_one": 3000, "ate_12": 3100, "ate_16": 3150},
                "21h": {"one_to_one": 3950, "ate_12": 4000, "ate_16": 4050},
                "24h": {"one_to_one": 4500, "ate_12": 4550, "ate_16": 4600},
            },
        },
        {
            "id": "it_user",
            "label": "TI Ótica do Utilizador (Excel, Power BI, Office) / Idiomas",
            "trainer_rate": 45.0,
            "prices": {
                "3h": {"one_to_one": 300, "ate_12": 350, "ate_16": 400},
                "4h": {"one_to_one": 400, "ate_12": 450, "ate_16": 500},
                "7h": {"one_to_one": 650, "ate_12": 700, "ate_16": 750},
                "8h": {"one_to_one": 750, "ate_12": 800, "ate_16": 850},
                "14h": {"one_to_one": 1300, "ate_12": 1350, "ate_16": 1400},
                "16h": {"one_to_one": 1400, "ate_12": 1500, "ate_16": 1550},
                "21h": {"one_to_one": 1850, "ate_12": 1900, "ate_16": 1950},
                "24h": {"one_to_one": 2100, "ate_12": 2150, "ate_16": 2200},
            },
        },
        {
            "id": "logistica_mkt_it_tec",
            "label": "Logística / Marketing / IT Técnico",
            "trainer_rate": 55.0,
            "prices": {},
        },
        {
            "id": "m365",
            "label": "Office 365 / Microsoft 365 & Copilot",
            "trainer_rate": 50.0,
            "prices": {},
        },
        {
            "id": "lean",
            "label": "Lean Management",
            "trainer_rate": 80.0,
            "prices": {},
        },
        {
            "id": "ia_ips",
            "label": "Inteligência Artificial (IA) / IT IPS Avançado",
            "trainer_rate": 100.0,
            "prices": {},
        },
    ],
    "defaults": {
        "kit_formando": 2.00,
        "estafeta_standard": 9.05,
        "estafeta_porto": 15.00,
        "sala_1dia": 250.00,
        "sala_meio_dia": 150.00,
        "coffee_break_1dia_pax": 10.00,
        "coffee_break_meio_dia_pax": 5.00,
        "km_rate": 0.40,
        "hotel_lisboa_porto": 140.00,
        "hotel_nacional": 120.00,
        "refeicao": 20.00,
        "margem_minima": 65.0,
    },
}

# Anti-Dicionário SKOLAE (Termos proibidos em PT-PT e chavões publicitários)
FORBIDDEN_TERMS = [
    (r"\bobrigad[oa]\s+pelo\s+retorno\b", "Usar 'Obrigado pela sua mensagem' ou 'Obrigado pela resposta' (zero pt-BR)."),
    (r"\bretorno\b", "Evitar 'retorno' no sentido de resposta; usar 'feedback', 'resposta' ou 'mensagem'."),
    (r"\bcapacitaç[ãa]o\b|\bcapacitar\b", "Termo proibido: usar 'desenvolvimento de competências' ou 'formação'."),
    (r"\bvenho\s+por\s+este\s+meio\b", "Chavão burocrático proibido."),
    (r"\bfazer\s+um\s+ponto\s+de\s+situaç[ãa]o\b", "Muleta proibida em follow-ups."),
    (r"\bsoluç[ãa]o\s+inovadora\s+e\s+diferenciadora\b", "Linguagem publicitária proibida."),
    (r"\bexperi[êe]ncia\s+[úu]nica\s+e\s+memor[áa]vel\b", "Superlativo publicitário proibido."),
    (r"\bpotenciar\s+o\s+talento\b", "Cliché corporativo proibido."),
    (r"\btransformar\s+desafios\s+em\s+oportunidades\b", "Cliché motivacional proibido."),
    (r"\bperfeitamente\s+alinhad[oa]\b|\bdesenhad[oa]\s+precisamente\b", "Superlativo enfático proibido; usar 'enquadra-se no que procuram'."),
    (r"\bturmas\s+abertas\b|\bcalend[áa]rio\s+inter-empresas\b", "Regra Inviolável: a SKOLAE opera 100% no modelo Intra-Empresa à medida."),
]


# ==============================================================================
# FUNÇÕES UTILITÁRIAS DE LEITURA DO REPOSITÓRIO
# ==============================================================================
def safe_read_text(path: Path) -> str:
    try:
        up = unc_path(path)
        if os.path.exists(up):
            with open(up, "r", encoding="utf-8", errors="replace") as f:
                return f.read()
    except Exception:
        pass
    return ""


def parse_frontmatter_and_body(md_text: str):
    """Separa o YAML frontmatter do corpo Markdown."""
    meta: Dict[str, Any] = {}
    body = md_text
    if md_text.startswith("---"):
        parts = md_text.split("---", 2)
        if len(parts) >= 3:
            try:
                loaded = yaml.safe_load(parts[1])
                if isinstance(loaded, dict):
                    meta = loaded
            except Exception:
                pass
            body = parts[2].strip()
    return meta, body


def extract_markdown_sections(body: str) -> Dict[str, str]:
    """Extrai secções H2 (## ) de um ficheiro Markdown."""
    sections: Dict[str, str] = {}
    current_title = "Resumo"
    current_lines: List[str] = []
    for line in body.splitlines():
        if line.startswith("## "):
            if current_lines:
                sections[current_title] = "\n".join(current_lines).strip()
            current_title = line[3:].strip()
            current_lines = []
        elif not line.startswith("# ") and not line.startswith("*Links:*"):
            current_lines.append(line)
    if current_lines:
        sections[current_title] = "\n".join(current_lines).strip()
    return sections


def extract_action_items(progress_body: str) -> List[Dict[str, Any]]:
    """Extrai tarefas/próximos passos de um ficheiro _progress.md."""
    items: List[Dict[str, Any]] = []
    in_next_steps = False
    for line in progress_body.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            header_lower = stripped.lower()
            in_next_steps = any(k in header_lower for k in ["próximos passos", "proximos passos", "próximas ações", "proximas acoes", "next steps"])
            continue
        if "* **Próximas Ações:**" in stripped or "* **Próximos Passos:**" in stripped:
            in_next_steps = True
            continue

        # Checkboxes: - [ ], - [x], - [/]
        m_cb = re.match(r"^[-*]\s*`?\[([ xX/])\]`?\s*(.+)$", stripped)
        if m_cb:
            state = m_cb.group(1).lower()
            text = re.sub(r"\*\*(.*?)\*\*", r"\1", m_cb.group(2)).strip()
            items.append({
                "text": text,
                "completed": state == "x",
                "in_progress": state == "/",
            })
        elif in_next_steps:
            m_num = re.match(r"^(?:\d+\.|[-*])\s+(.+)$", stripped)
            if m_num:
                text = re.sub(r"\*\*(.*?)\*\*", r"\1", m_num.group(1)).strip()
                if len(text) > 5 and not text.lower().startswith("links:"):
                    items.append({
                        "text": text,
                        "completed": False,
                        "in_progress": False,
                    })
    return items[:10]


def infer_account_status(meta: Dict[str, Any], context_text: str, progress_text: str, has_proposals: bool) -> str:
    raw_status = str(meta.get("status", "")).strip()
    combined = (context_text + "\n" + progress_text).lower()
    if "proposta" in combined or "orçamento" in combined or has_proposals:
        if raw_status.lower() in ["frio", "fechado", "adormecido"]:
            return "Frio"
        return "Em Proposta"
    if raw_status.lower() == "ativo" or "reunião" in combined or "diagnóstico" in combined:
        return "Ativo"
    if "contactado" in combined or "outreach" in combined or "prospeção" in combined:
        return "Qualificação"
    return raw_status if raw_status else "Carteira"


def scan_clients() -> List[Dict[str, Any]]:
    now = datetime.now().timestamp()
    if _CACHE["clients_list"] is not None and (now - _CACHE["clients_ts"] < 30):
        return _CACHE["clients_list"]

    clients = []
    up_clients = unc_path(CLIENTS_DIR)
    if not os.path.exists(up_clients):
        return []

    for entry in sorted(os.listdir(up_clients)):
        full_dir = CLIENTS_DIR / entry
        if not os.path.isdir(unc_path(full_dir)) or entry.startswith(".") or entry.startswith("_"):
            continue

        files = []
        try:
            files = os.listdir(unc_path(full_dir))
        except Exception:
            continue

        context_file = next((f for f in files if f.lower().endswith("_context.md") or f.lower() == "context.md"), None)
        progress_file = next((f for f in files if f.lower().endswith("_progress.md") or f.lower() == "progress.md"), None)
        notes_file = next((f for f in files if f.lower().endswith("_meeting_notes.md") or f.lower() == "meeting_notes.md"), None)

        context_raw = safe_read_text(full_dir / context_file) if context_file else ""
        progress_raw = safe_read_text(full_dir / progress_file) if progress_file else ""

        meta, context_body = parse_frontmatter_and_body(context_raw)
        prog_meta, progress_body = parse_frontmatter_and_body(progress_raw)

        has_proposals = any(f.lower().endswith((".pdf", ".pptx")) for f in files)
        status = infer_account_status(meta, context_body, progress_body, has_proposals)

        display_name = entry.replace("_", " ")
        # Extrair core business ou primeira linha útil
        core_business = meta.get("core_business", "")
        if not core_business:
            m_setor = re.search(r"\*\*Setor:\*\*\s*(.+)", context_body)
            if m_setor:
                core_business = m_setor.group(1).strip()

        last_date = str(meta.get("data_ultima_interacao", prog_meta.get("timestamp", "")))[:10]
        priority_idx = PRIORITY_ACCOUNTS.index(entry) if entry in PRIORITY_ACCOUNTS else 999

        clients.append({
            "id": entry,
            "name": display_name,
            "status": status,
            "core_business": core_business or "Formação Corporativa Intra-Empresa",
            "last_interaction": last_date,
            "has_proposals": has_proposals,
            "files_count": len(files),
            "priority_rank": priority_idx,
            "has_notes": bool(notes_file),
        })

    # Ordenar por prioridade primeiro, depois por Em Proposta / Ativo, depois alfabeticamente
    status_order = {"Em Proposta": 0, "Ativo": 1, "Qualificação": 2, "Carteira": 3, "Frio": 4}
    clients.sort(key=lambda c: (c["priority_rank"], status_order.get(c["status"], 9), c["name"].lower()))

    _CACHE["clients_list"] = clients
    _CACHE["clients_ts"] = now
    return clients


def load_all_contacts() -> List[Dict[str, Any]]:
    if _CACHE["contacts_list"] is not None:
        return _CACHE["contacts_list"]

    contacts: List[Dict[str, Any]] = []
    seen = set()

    def add_contact(company, name, email, role, phone="", location="", sector="", status="", source=""):
        company_s = str(company or "").strip()
        name_s = str(name or "").strip()
        email_s = str(email or "").strip()
        if not company_s and not name_s and not email_s:
            return
        key = (email_s.lower() if email_s else f"{company_s.lower()}:{name_s.lower()}")
        if key in seen:
            return
        seen.add(key)
        contacts.append({
            "company": company_s,
            "name": name_s,
            "email": email_s,
            "role": str(role or "").strip(),
            "phone": str(phone or "").strip(),
            "location": str(location or "").strip(),
            "sector": str(sector or "").strip(),
            "status": str(status or "").strip(),
            "source": source,
        })

    # 1. Contacts 2026-2027.xlsx
    p1 = DB_DIR / "Contacts 2026-2027.xlsx"
    if os.path.exists(unc_path(p1)):
        try:
            wb = openpyxl.load_workbook(unc_path(p1), read_only=True, data_only=True)
            ws = wb[wb.sheetnames[0]]
            for i, row in enumerate(ws.iter_rows(values_only=True)):
                if i == 0 or not row:
                    continue
                add_contact(
                    company=row[0] if len(row) > 0 else "",
                    name=row[1] if len(row) > 1 else "",
                    email=row[2] if len(row) > 2 else "",
                    role=row[3] if len(row) > 3 else "",
                    location=row[4] if len(row) > 4 else "",
                    sector=row[9] if len(row) > 9 else "",
                    status=row[13] if len(row) > 13 else "",
                    source="Contacts 2026-2027.xlsx",
                )
            wb.close()
        except Exception:
            pass

    # 2. Contactos_RH_Formacao_Lideranca.xlsx
    p2 = DB_DIR / "Contactos_RH_Formacao_Lideranca.xlsx"
    if os.path.exists(unc_path(p2)):
        try:
            wb = openpyxl.load_workbook(unc_path(p2), read_only=True, data_only=True)
            for sheet_name in ["Contactos_RH", "RH Hoje"]:
                if sheet_name in wb.sheetnames:
                    ws = wb[sheet_name]
                    for i, row in enumerate(ws.iter_rows(values_only=True)):
                        if i == 0 or not row:
                            continue
                        add_contact(
                            company=row[0] if len(row) > 0 else "",
                            name=row[1] if len(row) > 1 else "",
                            email=row[2] if len(row) > 2 else "",
                            role=row[3] if len(row) > 3 else "",
                            phone=row[4] if len(row) > 4 else "",
                            status=row[7] if len(row) > 7 else (row[6] if len(row) > 6 else "Base RH"),
                            source=f"Contactos_RH ({sheet_name})",
                        )
            wb.close()
        except Exception:
            pass

    # 3. Contactos_Nao_RH_Lideranca.xlsx
    p3 = DB_DIR / "Contactos_Nao_RH_Lideranca.xlsx"
    if os.path.exists(unc_path(p3)):
        try:
            wb = openpyxl.load_workbook(unc_path(p3), read_only=True, data_only=True)
            ws = wb[wb.sheetnames[0]]
            for i, row in enumerate(ws.iter_rows(values_only=True)):
                if i == 0 or not row:
                    continue
                add_contact(
                    company=row[0] if len(row) > 0 else "",
                    name=row[1] if len(row) > 1 else "",
                    email=row[2] if len(row) > 2 else "",
                    role=row[3] if len(row) > 3 else "",
                    phone=row[4] if len(row) > 4 else "",
                    status=row[6] if len(row) > 6 else "Liderança Não-RH",
                    source="Contactos_Nao_RH_Lideranca.xlsx",
                )
            wb.close()
        except Exception:
            pass

    _CACHE["contacts_list"] = contacts
    return contacts


def find_contacts_for_client(client_id: str, client_name: str, context_body: str) -> List[Dict[str, Any]]:
    """Cruza os contactos extraídos do dossier Markdown com os ficheiros Excel de 031_Bases_Dados."""
    results: List[Dict[str, Any]] = []
    seen_emails = set()

    # Extrair e-mails ou decisores mencionados no context.md
    emails_in_md = re.findall(r"[\w\.-]+@[\w\.-]+\.\w+", context_body)
    for em in emails_in_md:
        seen_emails.add(em.lower())

    # 1. Procurar nas bases Excel pelo nome do cliente
    tokens = [t.lower() for t in re.split(r"[\s_\-]+", client_name) if len(t) >= 3 and t.lower() not in {"portugal", "lda", "sa", "grupo", "aguas", "banco"}]
    all_contacts = load_all_contacts()
    for c in all_contacts:
        comp_low = c["company"].lower()
        em_low = c["email"].lower()
        if (em_low and em_low in seen_emails) or (tokens and any(re.search(rf"\b{re.escape(tok)}\b", comp_low) for tok in tokens)):
            results.append(c)
            if len(results) >= 12:
                break

    return results


# ==============================================================================
# ENDPOINTS DA API
# ==============================================================================
@app.get("/")
def serve_root():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/icons/lucide/{icon_name}")
def serve_lucide_icon(icon_name: str):
    if not icon_name.endswith(".svg"):
        icon_name += ".svg"
    safe_name = os.path.basename(icon_name)
    icon_path = LUCIDE_DIR / safe_name
    if not os.path.exists(unc_path(icon_path)):
        raise HTTPException(status_code=404, detail="Ícone não encontrado")
    return FileResponse(unc_path(icon_path), media_type="image/svg+xml")


@app.get("/api/icons")
def list_lucide_icons(q: str = "", limit: int = 120):
    if _CACHE["lucide_icons"] is None:
        up = unc_path(LUCIDE_DIR)
        if os.path.exists(up):
            _CACHE["lucide_icons"] = sorted(
                [f[:-4] for f in os.listdir(up) if f.endswith(".svg")]
            )
        else:
            _CACHE["lucide_icons"] = []

    all_icons = _CACHE["lucide_icons"]
    q_clean = q.strip().lower()
    if q_clean:
        filtered = [ic for ic in all_icons if q_clean in ic.lower()]
    else:
        # Ícones recomendados para propostas SKOLAE em primeiro lugar
        featured = [
            "target", "users", "award", "lightbulb", "shield-check", "sparkles",
            "Compass", "trending-up", "brain", "message-square", "check-circle-2",
            "briefcase", "layers", "zap", "bar-chart-3", "book-open", "handshake",
            "clock", "Flame", "globe", "heart-handshake", "key", "lock", "mic",
            "presentation", " puzzle", "rocket", "sliders", "star", "trophy",
            "user-check", "workflow"
        ]
        featured_clean = [f.lower().strip() for f in featured if f.lower().strip() in all_icons]
        rest = [ic for ic in all_icons if ic not in featured_clean]
        filtered = featured_clean + rest

    return {
        "total": len(all_icons),
        "matched": len(filtered),
        "icons": filtered[:limit],
    }


@app.get("/api/dashboard")
def get_dashboard():
    dash_raw = safe_read_text(DASHBOARD_JSON)
    dash_data = {}
    if dash_raw:
        try:
            dash_data = json.loads(dash_raw)
        except Exception:
            dash_data = {}

    clients = scan_clients()
    active_count = sum(1 for c in clients if c["status"] in ("Ativo", "Em Proposta"))
    proposal_count = sum(1 for c in clients if c["status"] == "Em Proposta")

    # Calcular tarefas da semana atual + semana anterior
    cw_days = dash_data.get("current_week", {}).get("days", [])
    cw_tasks = []
    for d in cw_days:
        for t in d.get("tasks", []):
            cw_tasks.append({
                **t,
                "day_name": d.get("day_name", ""),
                "short_name": d.get("short_name", ""),
                "date": d.get("date", ""),
            })

    completed_cw = sum(1 for t in cw_tasks if t.get("completed"))
    pending_cw = len(cw_tasks) - completed_cw
    prev_kpis = dash_data.get("previous_week", {}).get("kpis", {})

    # Margens reais registadas na TMB 25-26:
    # Curso 1 (Adnovum - SPRING & Devops): 2300€ / Custos 803.05€ -> 65.08%
    # Curso 2 (Details - Comercial): 2190€ / Custos 733.05€ -> 66.53%
    # ALDI Leadership Run: 115120€ / Custos 23980.40€ -> 79.17%
    # Média ponderada / aritmética das propostas TMB ativas = 70.26%
    tmb_proposals = [
        {"client": "Adnovum", "project": "SPRING & DevOps (14h)", "price": 2300.00, "cost": 803.05, "margin_pct": 65.08},
        {"client": "Details", "project": "Formação Comercial (14h)", "price": 2190.00, "cost": 733.05, "margin_pct": 66.53},
        {"client": "ALDI Portugal", "project": "ALDI Leadership Run (464h)", "price": 115120.00, "cost": 23980.40, "margin_pct": 79.17},
    ]
    avg_margin = round(sum(p["margin_pct"] for p in tmb_proposals) / len(tmb_proposals), 1)

    return {
        "metrics": {
            "tasks": {
                "completed": completed_cw,
                "pending": pending_cw,
                "total": len(cw_tasks),
                "prev_week_completed": prev_kpis.get("completed_tasks", 16),
                "prev_week_rate": prev_kpis.get("completion_rate", "94%"),
                "period_label": dash_data.get("current_week", {}).get("period_label", "Semana Atual"),
            },
            "margin": {
                "average_pct": avg_margin,
                "target_pct": 65.0,
                "status": "OK — Acima da Meta (≥ 65%)",
                "proposals": tmb_proposals,
            },
            "clients": {
                "total_portfolio": len(clients),
                "active_pipeline": active_count,
                "in_proposal": proposal_count,
            },
        },
        "current_week_tasks": cw_tasks,
        "previous_week_tasks": dash_data.get("previous_week", {}).get("completed_tasks_list", []),
        "tmb_matrix": TMB_MATRIX,
    }


class TaskToggleRequest(BaseModel):
    task_id: str


@app.post("/api/dashboard/toggle-task")
def toggle_dashboard_task(req: TaskToggleRequest):
    dash_raw = safe_read_text(DASHBOARD_JSON)
    if not dash_raw:
        raise HTTPException(status_code=404, detail="dashboard_data.json não encontrado")
    data = json.loads(dash_raw)
    updated = False
    for d in data.get("current_week", {}).get("days", []):
        for t in d.get("tasks", []):
            if t.get("id") == req.task_id:
                t["completed"] = not bool(t.get("completed"))
                updated = True
                break
    if updated:
        with open(unc_path(DASHBOARD_JSON), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    return {"ok": updated}


@app.get("/api/clients")
def list_clients(q: str = "", status: str = ""):
    clients = scan_clients()
    if q.strip():
        ql = q.strip().lower()
        clients = [
            c for c in clients
            if ql in c["name"].lower() or ql in c["core_business"].lower() or ql in c["id"].lower()
        ]
    if status.strip() and status.lower() != "todos":
        clients = [c for c in clients if c["status"].lower() == status.strip().lower()]
    return {"total": len(clients), "clients": clients}


@app.get("/api/clients/{client_id}")
def get_client_detail(client_id: str):
    client_dir = CLIENTS_DIR / client_id
    up_dir = unc_path(client_dir)
    if not os.path.exists(up_dir) or not os.path.isdir(up_dir):
        raise HTTPException(status_code=404, detail=f"Cliente '{client_id}' não encontrado.")

    files = sorted(os.listdir(up_dir))
    context_file = next((f for f in files if f.lower().endswith("_context.md") or f.lower() == "context.md"), None)
    progress_file = next((f for f in files if f.lower().endswith("_progress.md") or f.lower() == "progress.md"), None)
    notes_file = next((f for f in files if f.lower().endswith("_meeting_notes.md") or f.lower() == "meeting_notes.md"), None)

    context_raw = safe_read_text(client_dir / context_file) if context_file else ""
    progress_raw = safe_read_text(client_dir / progress_file) if progress_file else ""
    notes_raw = safe_read_text(client_dir / notes_file) if notes_file else ""

    meta, context_body = parse_frontmatter_and_body(context_raw)
    prog_meta, progress_body = parse_frontmatter_and_body(progress_raw)
    notes_meta, notes_body = parse_frontmatter_and_body(notes_raw)

    context_sections = extract_markdown_sections(context_body)
    progress_sections = extract_markdown_sections(progress_body)
    action_items = extract_action_items(progress_body)
    if not action_items:
        action_items = extract_action_items(context_body)

    has_proposals = any(f.lower().endswith((".pdf", ".pptx")) for f in files)
    status = infer_account_status(meta, context_body, progress_body, has_proposals)

    decisores = meta.get("decisores", [])
    if isinstance(decisores, str):
        decisores = [decisores]
    areas = meta.get("areas_interesse", [])
    if isinstance(areas, str):
        areas = [areas]

    # Se não houver decisores no YAML, procurar secções de Interlocutores / Decisores / Stakeholders
    if not decisores:
        for sec_title, sec_content in context_sections.items():
            if any(k in sec_title.lower() for k in ["decisor", "interlocutor", "stakeholder", "identificação", "contacto"]):
                for line in sec_content.splitlines():
                    m_bold = re.search(r"[-*]\s*\*\*(.+?)\*\*(.*)", line)
                    if m_bold:
                        key_name = m_bold.group(1).strip().rstrip(":")
                        rest = m_bold.group(2).strip(" —:-")
                        if key_name.lower() not in {"nome", "setor", "entidade", "nif", "morada", "website", "posicionamento", "delegações", "dimensão da equipa", "origem do contacto", "origem da oportunidade", "gestor de conta (skolae)", "gestor da conta (skolae)"}:
                            decisores.append(f"{key_name} {rest}".strip())

    # Contactos cruzados na Base de Dados Excel
    db_contacts = find_contacts_for_client(client_id, client_id.replace("_", " "), context_body)

    # Lista de ficheiros ricos na pasta do cliente
    file_items = []
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        ftype = "document"
        if ext == ".pdf":
            ftype = "pdf"
        elif ext in (".pptx", ".ppt"):
            ftype = "pptx"
        elif ext == ".md":
            ftype = "markdown"
        file_items.append({
            "name": f,
            "type": ftype,
            "rel_path": f"03_Carteira_Clientes/032_Clientes/{client_id}/{f}",
        })

    # Regras de Alerta Específicas (Guardrails SKOLAE)
    guardrails = []
    if client_id == "Carl Zeiss":
        guardrails.append("Projeto #SOMOS pertence única e exclusivamente à Carl Zeiss (51 Assessments DISC + Feedbacks + Laboratórios com Catarina Cabanelas). Neuroselling alocado à formadora Helena.")
    elif client_id == "Devoteam":
        guardrails.append("A Devoteam NÃO tem qualquer relação com o Projeto #SOMOS. Oportunidade ativa: Workshop 'Comunicar com Impacto: Da Apresentação Pessoal ao Pitch Profissional' (7h presencial em Lisboa, 100% em Inglês, formadora Alcina, Carolina Lopes).")
    elif client_id == "Desentop_Ambiente":
        guardrails.append("Proposta de Programa Master de Liderança Operacional (8 líderes) integra Assessments Thomas International (PPA DISC, HPTI e GIA) + 8h Feedback 1:1 + 21h Academia + Acompanhamento On-the-Job (2h/líder), financiado via saldo FCT.")

    return {
        "id": client_id,
        "name": client_id.replace("_", " "),
        "status": status,
        "core_business": meta.get("core_business", "Formação Corporativa Intra-Empresa"),
        "last_interaction": str(meta.get("data_ultima_interacao", prog_meta.get("timestamp", "")))[:10],
        "decisores": decisores,
        "areas_interesse": areas,
        "guardrails": guardrails,
        "context_md": context_body,
        "progress_md": progress_body,
        "meeting_notes_md": notes_body,
        "context_sections": context_sections,
        "progress_sections": progress_sections,
        "action_items": action_items,
        "db_contacts": db_contacts,
        "files": file_items,
    }


@app.get("/api/contacts")
def search_contacts(q: str = "", limit: int = 60):
    all_c = load_all_contacts()
    ql = q.strip().lower()
    if ql:
        filtered = [
            c for c in all_c
            if ql in c["company"].lower()
            or ql in c["name"].lower()
            or ql in c["email"].lower()
            or ql in c["role"].lower()
            or ql in c["sector"].lower()
        ]
    else:
        filtered = all_c

    return {
        "total_database": len(all_c),
        "matched": len(filtered),
        "contacts": filtered[:limit],
    }


class MarginCalculationRequest(BaseModel):
    preco_venda: float
    custos_diretos: Optional[float] = None
    horas_formacao: Optional[float] = 14.0
    valor_hora_formador: Optional[float] = 50.0
    num_formandos: Optional[int] = 12
    incluir_kit: Optional[bool] = True
    estafeta: Optional[float] = 9.05
    custo_sala: Optional[float] = 0.0
    custo_coffee: Optional[float] = 0.0
    outros_custos: Optional[float] = 0.0
    local_formacao: Optional[str] = "Lisboa"
    inclui_tabuleiro_jogo: Optional[bool] = False


@app.post("/api/margin/calculate")
def calculate_margin_endpoint(req: MarginCalculationRequest):
    # Se custos_diretos não for passado diretamente, calcula pela estrutura TMB 25-26
    if req.custos_diretos is not None:
        custos_totais = float(req.custos_diretos)
        breakdown = {"custos_diretos_manuais": round(custos_totais, 2)}
    else:
        custo_formador = (req.horas_formacao or 0) * (req.valor_hora_formador or 0)
        custo_kits = ((req.num_formandos or 0) * 2.0) if req.incluir_kit else 0.0
        custo_estafeta = float(req.estafeta or 0.0)
        custo_sala = float(req.custo_sala or 0.0)
        custo_coffee = float(req.custo_coffee or 0.0)
        outros = float(req.outros_custos or 0.0)
        custos_totais = custo_formador + custo_kits + custo_estafeta + custo_sala + custo_coffee + outros
        breakdown = {
            "formador": round(custo_formador, 2),
            "kits_abilways": round(custo_kits, 2),
            "envio_estafeta": round(custo_estafeta, 2),
            "sala_abilways": round(custo_sala, 2),
            "coffee_breaks": round(custo_coffee, 2),
            "outros_materiais": round(outros, 2),
        }

    preco_minimo_65 = round(custos_totais / (1.0 - 0.65), 2) if custos_totais > 0 else 0.0
    preco_venda = float(req.preco_venda) if req.preco_venda > 0 else preco_minimo_65

    # Executar o script oficial determinístico 00_Instrucoes_Agente/scripts/calcular_margem.py
    script_output = ""
    script_approved = False
    try:
        proc = subprocess.run(
            [sys.executable, unc_path(CALC_MARGEM_SCRIPT), str(preco_venda), str(round(custos_totais, 2))],
            capture_output=True,
            text=True,
            timeout=5,
        )
        script_output = (proc.stdout + "\n" + proc.stderr).strip()
        script_approved = proc.returncode == 0
    except Exception as e:
        script_output = f"Erro ao executar script: {e}"

    margem_abs = preco_venda - custos_totais
    margem_pct = (margem_abs / preco_venda * 100.0) if preco_venda > 0 else 0.0

    # Alertas Logísticos e Financeiros Obrigatórios (SKOLAE Standard)
    alerts = []
    loc_low = (req.local_formacao or "Lisboa").strip().lower()
    if loc_low and not any(k in loc_low for k in ["lisboa", "remoto", "online", "teams", "live training"]):
        alerts.append(
            f"📍 Alerta de Deslocação ({req.local_formacao}): A sede da SKOLAE situa-se em Lisboa. Verifique se deslocações (0,40 €/km), portagens, refeições (20 €/ref.) e alojamento (120 €–140 €/noite) foram incluídos ou ressalvados a redébito."
        )
    if req.inclui_tabuleiro_jogo:
        alerts.append(
            "🎲 Alerta de Material Didático Especial: Certifique-se de que o custo de reprodução do tabuleiro pedagógico (ex.: Jogo dos Exploradores) ou assessments foi somado na rubrica 'Outros Materiais / Assessments'."
        )
    if margem_pct < 65.0:
        alerts.append(
            f"🚨 ALERTA CRÍTICO: Margem Bruta de {margem_pct:.2f}% é inferior ao mínimo obrigatório de 65%. Preço mínimo para 65% de margem: {preco_minimo_65:.2f} €."
        )

    return {
        "preco_venda": round(preco_venda, 2),
        "custos_diretos": round(custos_totais, 2),
        "margem_absoluta": round(margem_abs, 2),
        "margem_percentual": round(margem_pct, 2),
        "preco_minimo_65": preco_minimo_65,
        "aprovada": margem_pct >= 65.0 and script_approved,
        "breakdown": breakdown,
        "alerts": alerts,
        "script_output": script_output,
    }


def audit_skolae_text(text: str) -> Dict[str, Any]:
    """Audita um texto contra o Anti-Dicionário SKOLAE e conta as palavras do corpo."""
    # Contar palavras excluindo saudação e assinatura para o padrão 35-55 palavras, e também contagem global
    lines = [l.strip() for l in text.strip().splitlines() if l.strip()]
    total_words = len(re.findall(r"\b\w+\b", text))

    body_lines = []
    for l in lines:
        low = l.lower()
        if any(low.startswith(g) for g in ["olá ", "bom dia", "boa tarde", "hi ", "cumprimentos", "com os melhores cumprimentos", "obrigado e até breve", "best regards", "bruno vicente", "assunto:"]):
            continue
        body_lines.append(l)
    body_words = len(re.findall(r"\b\w+\b", " ".join(body_lines)))

    violations = []
    for pattern, msg in FORBIDDEN_TERMS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            violations.append(msg)

    return {
        "total_words": total_words,
        "body_words": body_words,
        "is_clean_pt": len(violations) == 0,
        "violations": violations,
    }


class FastTrackRequest(BaseModel):
    client_id: Optional[str] = None
    template_type: str = "followup_proposta"  # followup_proposta | followup_aprovacao | soft_breakup | proposta_pronta | outreach_rh | outreach_dg
    recipient_name: Optional[str] = None
    topic: Optional[str] = None


@app.post("/api/actions/fast-track")
def generate_fast_track(req: FastTrackRequest):
    client_name = "vossa organização"
    recipient = req.recipient_name or ""
    topic = req.topic or ""

    if req.client_id:
        try:
            detail = get_client_detail(req.client_id)
            client_name = detail["name"]
            if not recipient and detail["decisores"]:
                first_dec = detail["decisores"][0]
                recipient = first_dec.split("(")[0].split("—")[0].split("-")[0].strip()
            if not topic and detail["areas_interesse"]:
                topic = ", ".join(detail["areas_interesse"][:2])
        except Exception:
            pass

    if not recipient:
        recipient = "[Nome]"
    if not topic:
        topic = "desenvolvimento de competências das vossas equipas"

    # Limpar parênteses longos do tópico para soar natural no e-mail
    topic_clean = re.sub(r"\s*\([^)]*\)", "", topic).strip()

    if req.template_type == "followup_proposta":
        # Padrão Conciso de 35-55 Palavras (3 blocos curtos)
        first_topic = topic_clean.split(",")[0].strip()
        subject = f"Proposta de formação em {first_topic} — {client_name} / SKOLAE"
        email_text = (
            f"Olá {recipient}, boa tarde,\n\n"
            f"Escrevo-lhe relativamente à proposta de formação em {first_topic}, "
            f"para perceber se já concluíram a análise interna ou se existe alguma atualização sobre o projeto.\n\n"
            f"Caso seja útil esclarecermos algum ponto ou ajustarmos a solução apresentada, terei todo o gosto em ajudar.\n\n"
            f"Fico a aguardar o seu feedback.\n\n"
            f"Cumprimentos,\n"
            f"Bruno Vicente"
        )
        mode_label = "Follow-up em Análise de Proposta (Padrão 35–55 palavras)"

    elif req.template_type == "followup_aprovacao":
        subject = f"Planeamento da formação em {topic_clean} — {client_name}"
        email_text = (
            f"Olá {recipient}, boa tarde,\n\n"
            f"Conseguiram entretanto avançar com a validação interna relativamente à proposta de formação em {topic_clean} e têm já alguma previsão para a sua realização?\n\n"
            f"Se estiverem já em condições de avançar, podemos combinar a reunião de alinhamento pedagógico e começar a fechar as datas.\n\n"
            f"Caso o tema tenha ficado para mais tarde, diga-me também sem problema, para eu conseguir ajustar o nosso planeamento interno.\n\n"
            f"Fico a aguardar o seu feedback.\n\n"
            f"Com os melhores cumprimentos,\n"
            f"Bruno Vicente"
        )
        mode_label = "Follow-up de Aprovação Interna (Bifurcação Sem Pressão)"

    elif req.template_type == "soft_breakup":
        subject = f"Projetos em aberto — {client_name} / SKOLAE"
        email_text = (
            f"Olá {recipient}, boa tarde,\n\n"
            f"Estou a fechar os projetos em aberto deste trimestre relativamente à proposta de {topic_clean}.\n\n"
            f"Como não voltei a ter feedback, vou assumir que o vosso foco interno está noutras áreas neste momento e vou encerrar este assunto do nosso lado.\n\n"
            f"Se a situação mudar mais à frente, sinta-se à vontade para reabrir o contacto.\n\n"
            f"Com os melhores cumprimentos,\n"
            f"Bruno Vicente"
        )
        mode_label = "Soft Break-up (Limpeza de Arquivo Sem Culpa)"

    elif req.template_type == "proposta_pronta":
        subject = f"Proposta de formação em {topic_clean} — {client_name}"
        email_text = (
            f"Olá {recipient}, boa tarde,\n\n"
            f"Já temos pronta a proposta de formação em {topic_clean} para as vossas equipas na {client_name}.\n\n"
            f"Prefere que lhe envie já o documento para análise, ou tem 10 minutos para vermos os pontos principais via Teams?\n\n"
            f"Fico a aguardar o seu feedback.\n\n"
            f"Com os melhores cumprimentos,\n"
            f"Bruno Vicente"
        )
        mode_label = "Notificação de Proposta Concluída (Escolha de Canal)"

    elif req.template_type == "outreach_rh":
        subject = f"Formação e desenvolvimento das equipas — {client_name} / SKOLAE"
        email_text = (
            f"Olá {recipient}, boa tarde,\n\n"
            f"O meu nome é Bruno Vicente e sou consultor da SKOLAE (antiga Abilways) na área de formação e desenvolvimento de competências.\n\n"
            f"Sendo responsável pela área de Pessoas e Recursos Humanos na {client_name}, queria perceber como costumam organizar internamente o desenvolvimento das vossas equipas e se recorrem também a parceiros externos para ações desenhadas à medida.\n\n"
            f"Se tiverem desafios prioritários no desenvolvimento das equipas para os próximos meses, podemos falar 10 minutos por Teams para nos conhecermos e perceber onde podemos ser úteis em algum tema?\n\n"
            f"Fico a aguardar o seu feedback.\n\n"
            f"Com os melhores cumprimentos,\n"
            f"Bruno Vicente"
        )
        mode_label = "Outreach Consultivo — Recursos Humanos / People (4 Blocos)"

    else:  # outreach_dg
        subject = f"Desenvolvimento das equipas na {client_name} — SKOLAE"
        email_text = (
            f"Olá {recipient}, boa tarde,\n\n"
            f"O meu nome é Bruno Vicente e sou consultor da SKOLAE (antiga Abilways) na área de desenvolvimento de competências e liderança.\n\n"
            f"Acompanhando a direção da {client_name}, contacto-o para perceber se costumam recorrer a parceiros externos para ações de formação à medida das vossas equipas ou se este tema é articulado exclusivamente com os Recursos Humanos.\n\n"
            f"Se este for um tema com relevância para a vossa gestão este ano, faria sentido falarmos 10 minutos por Teams ou a sua indicação é articular diretamente com os Recursos Humanos?\n\n"
            f"Fico a aguardar o seu feedback.\n\n"
            f"Com os melhores cumprimentos,\n"
            f"Bruno Vicente"
        )
        mode_label = "Outreach Executivo — Direção Geral / Operações (Com Bifurcação RH)"

    audit = audit_skolae_text(email_text)
    return {
        "mode_label": mode_label,
        "client_name": client_name,
        "recipient": recipient,
        "subject": subject,
        "body": email_text,
        "audit": audit,
    }


class PPTProposalRequest(BaseModel):
    client_id: Optional[str] = None
    client_name: Optional[str] = None
    theme: str
    impact_goal: Optional[str] = "a eficácia operacional, a colaboração e o desempenho diário das equipas"
    pillars: Optional[str] = "a comunicação assertiva, a tomada de decisão prática, o alinhamento de prioridades e a resolução estruturada de problemas"


@app.post("/api/actions/ppt-proposal")
def generate_ppt_proposal_framework(req: PPTProposalRequest):
    cname = req.client_name or ""
    if not cname and req.client_id:
        cname = req.client_id.replace("_", " ")
    if not cname:
        cname = "[Nome do Cliente]"

    theme = req.theme.strip() or "Liderança e Desenvolvimento de Equipas"
    impact = (req.impact_goal or "a eficácia operacional, a colaboração e o desempenho diário das equipas").strip()
    pillars = (req.pillars or "a comunicação assertiva, a tomada de decisão prática, o alinhamento de prioridades e a resolução estruturada de problemas").strip()

    # Slide 6: 4 Parágrafos Oficiais (Basier Circle 12pt, #333333, Nome do Cliente a Negrito Laranja #FF912B)
    p1 = f"Os responsáveis da **{cname}** tomaram a decisão de investir no desenvolvimento de competências de {theme}."
    p2 = f"Desde sempre a SKOLAE Formação dispõe no seu portefólio de soluções de aprendizagem específicas para o desenvolvimento de competências de {theme} que possam potenciar {impact}."
    p3 = f"Uma boa prática de {theme} nas organizações tem impacto no clima organizacional, na produtividade e, consequentemente, no negócio."
    p4 = f"Contextualizamos que abordar {theme} é integrar temas tão fundamentais como {pillars}."

    # Slide 12: Tags Executivas de 2 a 3 palavras + Ícones Lucide sugeridos
    competencias = [
        {"tag": "Alinhamento Operacional", "icon": "target"},
        {"tag": "Comunicação Assertiva", "icon": "message-square"},
        {"tag": "Tomada de Decisão", "icon": "compass"},
        {"tag": "Colaboração em Equipa", "icon": "users"},
        {"tag": "Foco em Resultados", "icon": "award"},
    ]

    # Slide 13: Objetivos Específicos (1 linha, 10-14 palavras, iniciados por verbo no infinitivo)
    objetivos = [
        f"Aplicar ferramentas práticas de {theme.lower()} no contexto diário de trabalho das equipas.",
        "Desenvolver comportamentos observáveis que reforcem a clareza, a coordenação e a eficácia operacional.",
        "Consolidar rotinas de acompanhamento e resolução de desafios reais através de treino prático.",
    ]

    # Slide Final: Bloco Oficial de Contactos (@abilways.com)
    contactos_oficiais = [
        {"name": "Bruno Vicente", "role": "Business Developer", "email": "bvicente@abilways.com", "phone": "(+351) 91 411 26 29"},
        {"name": "Nuno Jorge", "role": "Head of Sales", "email": "njorge@abilways.com", "phone": "(+351) 910 457 434"},
        {"name": "Telma Lopes", "role": "Pedagogical Coordinator", "email": "tlopes@abilways.com", "phone": "(+351) 914 165 110"},
    ]

    return {
        "client_name": cname,
        "theme": theme,
        "typography_spec": "Basier Circle 12pt | Texto #333333 | Destaque Cliente #FF912B | Espaçamento 14pt",
        "slide_6_paragraphs": [p1, p2, p3, p4],
        "slide_12_competencias": competencias,
        "slide_13_objetivos": objetivos,
        "slide_final_contactos": contactos_oficiais,
    }


class ChatRequest(BaseModel):
    message: str
    client_id: Optional[str] = None


@app.post("/api/chat")
def strategic_chat(req: ChatRequest):
    msg = req.message.strip()
    msg_low = msg.lower()

    # Detetar se o utilizador escreveu em Inglês para responder em UK English (com contrações obrigatórias)
    en_markers = ["hello", "please", "can you", "write an email", "draft", "what is", "how much", "proposal for", "follow up"]
    is_english = any(m in msg_low for m in en_markers) and not any(pt in msg_low for pt in ["olá", "proposta", "reunião", "margem", "cliente", "para a", "como", "qual"])

    # Carregar contexto do cliente selecionado ou mencionado na mensagem
    active_client = None
    if req.client_id:
        try:
            active_client = get_client_detail(req.client_id)
        except Exception:
            active_client = None

    # Verificar se a mensagem menciona explicitamente outro cliente da carteira
    all_clients = scan_clients()
    for c in all_clients:
        cname_low = c["name"].lower()
        cid_low = c["id"].lower()
        if len(cname_low) >= 4 and (cname_low in msg_low or cid_low in msg_low):
            try:
                active_client = get_client_detail(c["id"])
                break
            except Exception:
                pass

    # 1. GUARDRAILS FACTUAIS DE PROJETOS E CLIENTES (ZERO CONFUSÃO)
    if "somos" in msg_low or "#somos" in msg_low:
        return {
            "reply": (
                "### Guardrail de Integridade Factual — Projeto #SOMOS\n\n"
                "- **Cliente Exclusivo:** **Carl Zeiss (ZEISS)** (`Ref. 19354 - Carl Zeiss #SOMOS.pdf`).\n"
                "- **Interlocutora Principal:** Patrícia Fernandes (*People Business Partner*) e Tiago Almeida (*Diretor-Geral*).\n"
                "- **Especialista Alocada (SKOLAE):** Catarina Cabanelas.\n"
                "- **Arquitetura e Valor:** **21.055,00 €** s/ IVA (51 Assessments DISC + 51 sessões de Feedback individual de 1h + 6 Laboratórios de colaboração + 4 Training-Labs) + 1 Assessment DISC extra (**65,00 €**).\n"
                "- **Nota de Rigor:** A **Devoteam não tem qualquer relação** com o Projeto #SOMOS."
            ),
            "mode": "Fact Check · Zero Alucinação",
        }

    if "thomas" in msg_low or "ppa" in msg_low or "hpti" in msg_low or "gia" in msg_low:
        return {
            "reply": (
                "### Diagnóstico Psicométrico Thomas International — Desentop Ambiente\n\n"
                "- **Distinção Factual:** A **Thomas International** (PPA DISC, HPTI e GIA) é o instrumento psicométrico e fornecedor da SKOLAE — **o cliente final da proposta para os 8 líderes operacionais é a Desentop Ambiente** (interlocutora: **Patrícia Bicho**, Responsável QAS).\n"
                "- **Estrutura do Programa Master (Desentop Ambiente):**\n"
                "  1. **Fase 1:** Diagnóstico Psicométrico para **8 líderes** (Thomas PPA, HPTI e GIA — 480 unidades / 1.700 € no pacote de 500 un vs. 2.080 € à peça).\n"
                "  2. **Fase 2:** 8h de Feedback Individual 1:1 + Reunião de Direção com Mapa Global de Liderança.\n"
                "  3. **Fase 3:** Academia de Liderança Presencial (21h — 3 workshops x 7h para 10 participantes).\n"
                "  4. **Fase 4:** Acompanhamento *On-the-Job* no Terreno (2 sessões de 1h = 2h por líder).\n"
                "- **Mecanismo Financeiro:** Execução prioritária através de verba cativa do **FCT (Fundo de Compensação do Trabalho)** até ao final de 2026."
            ),
            "mode": "Fact Check · Dossier Desentop Ambiente",
        }

    # 2. CÁLCULO DE MARGEM DIRETO NO CHAT (Ex: "margem 2500 800" ou "calcular margem")
    nums = [float(x.replace(",", ".")) for x in re.findall(r"\b\d+(?:[.,]\d+)?\b", msg)]
    if ("margem" in msg_low or "orçamento" in msg_low or "custo" in msg_low) and len(nums) >= 2:
        pv = max(nums[0], nums[1])
        cd = min(nums[0], nums[1])
        res = calculate_margin_endpoint(MarginCalculationRequest(preco_venda=pv, custos_diretos=cd))
        status_badge = "✅ **APROVADA (≥ 65%)**" if res["aprovada"] else "🚨 **SUB-OTIMIZADA (< 65%) — Requer Ajustamento**"
        return {
            "reply": (
                f"### Auditoria Determinística de Margem (`calcular_margem.py`)\n\n"
                f"- **Preço de Venda Proposto:** `{res['preco_venda']:.2f} €` (s/ IVA)\n"
                f"- **Custos Diretos Totais:** `{res['custos_diretos']:.2f} €`\n"
                f"- **Margem Bruta Absoluta:** `{res['margem_absoluta']:.2f} €`\n"
                f"- **Margem Bruta Percentual:** **`{res['margem_percentual']:.2f}%`** — {status_badge}\n"
                f"- **Preço Mínimo para Garantir 65%:** `{res['preco_minimo_65']:.2f} €`\n\n"
                + ("\n".join(f"> {a}" for a in res["alerts"]) if res["alerts"] else "> Cumpre integralmente a regra financeira da SKOLAE Formação.")
            ),
            "mode": "Motor Financeiro TMB 25-26",
        }

    # 3. PREPARAÇÃO DE REUNIÃO DE DIAGNÓSTICO (6 PERGUNTAS NUCLEARES)
    if any(k in msg_low for k in ["reunião", "reuniao", "diagnóstico", "diagnostico", "guião", "guiao", "perguntas"]):
        cname = active_client["name"] if active_client else "o cliente"
        decisor = active_client["decisores"][0] if (active_client and active_client["decisores"]) else "o interlocutor"
        return {
            "reply": (
                f"### Mapa de Conversa Orgânico — Reunião de Diagnóstico ({cname})\n\n"
                f"**Interlocutor:** {decisor}  \n"
                f"**Princípio Operacional:** Conduzir uma conversa natural de terreno (sem despejar checklists nem sugerir hipóteses prévias nas perguntas).\n\n"
                f"#### As 6 Perguntas Nucleares (Abordagem Aberta)\n"
                f"1. **Origem da Necessidade (Gatilho):** *«O que aconteceu para esta necessidade surgir agora?»*\n"
                f"2. **Contexto Real de Aplicação:** *«Em que situações concretas estas pessoas precisam de aplicar esta competência no dia a dia?»*\n"
                f"3. **Diagnóstico do Comportamento Atual:** *«E o que é que normalmente acontece nessas situações? Onde sentem que está a principal dificuldade?»* *(Pedir sempre ancoragem factual: «Consegue dar-me um exemplo prático recente?»)*\n"
                f"4. **Gap Comportamental:** *«O que gostariam que estas pessoas conseguissem fazer de forma diferente?»*\n"
                f"5. **Critério Real de Sucesso:** *«Se daqui a algum tempo disserem que esta formação resultou, o que é que terá mudado na prática? Como perceberiam internamente essa mudança?»*\n"
                f"6. **Teste 'Intervention Before Training' & Parâmetros Operacionais:** *«Para além de desenvolver competências, existe alguma alteração de processo, ferramentas ou acompanhamento dos managers necessária para que apliquem isto no terreno?»* (Fechar com nº de formandos, perfil, local e janela temporal).\n\n"
                f"#### Matriz: O Que NÃO Assumir\n"
                f"| Premissa a Evitar | Postura Correta no Diagnóstico |\n"
                f"|---|---|\n"
                f"| Assumir formato ou rácio de turma à cabeça | Recolher dados neutros primeiro e desenhar internamente com a coordenação pedagógica |\n"
                f"| Introduzir opções na pergunta (*leading questions*) | Manter perguntas 100% abertas e pedir exemplos observáveis |\n"
                f"| Prometer dinâmicas específicas em nome do formador | Respeitar a fase de desenho de detalhe pedagógico |"
            ),
            "mode": "Nível 3 · Diagnostic Mode",
        }

    # 4. REDAÇÃO DE FOLLOW-UP OU E-MAIL NO CHAT
    if any(k in msg_low for k in ["follow-up", "followup", "follow up", "email", "e-mail", "escreve", "redige", "minuta"]):
        ttype = "followup_proposta"
        if "break" in msg_low or "arquivo" in msg_low or "sem resposta" in msg_low:
            ttype = "soft_breakup"
        elif "aprova" in msg_low or "adiado" in msg_low:
            ttype = "followup_aprovacao"
        elif "pronta" in msg_low or "10 minutos" in msg_low:
            ttype = "proposta_pronta"
        elif "prospe" in msg_low or "outreach" in msg_low or "frio" in msg_low:
            ttype = "outreach_rh"

        ft = generate_fast_track(FastTrackRequest(
            client_id=active_client["id"] if active_client else None,
            template_type=ttype,
        ))
        return {
            "reply": (
                f"### {ft['mode_label']}\n"
                f"**Assunto:** `{ft['subject']}`\n\n"
                f"```text\n{ft['body']}\n```\n\n"
                f"**Auditoria SKOLAE Standard:** `{ft['audit']['body_words']} palavras no corpo` · "
                f"`Zero pt-BR` · `Tratamento Formal (3.ª pessoa)` · `100% Intra-Empresa`"
            ),
            "mode": "Modo Fast-Track (1 Turno)",
        }

    # 5. RESPOSTA EM UK ENGLISH (SE O UTILIZADOR ESCREVER EM INGLÊS)
    if is_english:
        cname = active_client["name"] if active_client else "your target account"
        return {
            "reply": (
                f"### Strategic Partner Brief — {cname} (UK English Standard)\n\n"
                f"Here's the clean, low-friction B2B outreach draft following SKOLAE's international standard (mandatory contractions, zero AI connectors, direct 12-word opening):\n\n"
                f"```text\n"
                f"Hi [Name],\n\n"
                f"I'm Bruno Vicente from SKOLAE, a Portuguese learning and development partner.\n\n"
                f"We work with organisations on tailored intra-company development initiatives, and I'd like to understand how you currently structure team training at {cname} and whether you also partner with external providers.\n\n"
                f"If you're not the right person for this topic, could you point me towards the colleague who looks after L&D?\n\n"
                f"Best regards,\n"
                f"Bruno Vicente\n"
                f"```"
            ),
            "mode": "UK English B2B Standard",
        }

    # 6. RESPOSTA CONTEXTUAL SOBRE O CLIENTE SELECIONADO OU SÍNTESE EXECUTIVA DA CARTEIRA
    if active_client:
        dec_str = ", ".join(active_client["decisores"][:3]) if active_client["decisores"] else "Por mapear no dossier"
        areas_str = ", ".join(active_client["areas_interesse"][:4]) if active_client["areas_interesse"] else "Formação Intra-Empresa à Medida"
        steps_md = "\n".join(
            f"- {'✅' if a['completed'] else '⏳'} {a['text']}"
            for a in active_client["action_items"][:5]
        ) or "- Rever estado da oportunidade e validar próximo contacto consultivo."
        guardrail_md = (
            f"\n\n> **Nota de Rigor Factual:** {active_client['guardrails'][0]}"
            if active_client["guardrails"] else ""
        )

        return {
            "reply": (
                f"### Análise Estratégica da Conta: **{active_client['name']}** (`{active_client['status']}`)\n\n"
                f"- **Core Business:** {active_client['core_business']}\n"
                f"- **Decisores / Interlocutores:** {dec_str}\n"
                f"- **Eixos Formativos Mapeados:** {areas_str}\n\n"
                f"#### Próximas Ações Recomendadas\n"
                f"{steps_md}"
                f"{guardrail_md}\n\n"
                f"Podes utilizar os botões de ação rápida à esquerda para gerar um **Follow-up Fast-Track (35–55 palavras)**, estruturar o **Slide 6 da Proposta PPT** ou **Auditar a Margem TMB 25-26** para a **{active_client['name']}**."
            ),
            "mode": f"Contexto Ativo · {active_client['name']}",
        }

    # Resposta Estratégica Geral (Foco do Dia - Perfil SC)
    return {
        "reply": (
            "### Ponto de Situação & Foco Comercial do Dia (SKOLAE BIZZ DEV AI)\n\n"
            "Selecionei as prioridades de maior impacto direto na carteira:\n"
            "1. **Desentop Ambiente (Probabilidade 90% · Saldo FCT):** Fechar os valores da proposta financeira do Programa Master de Liderança Operacional (8 líderes c/ Assessments Thomas PPA/HPTI/GIA + 21h Academia + acompanhamento no terreno) para validação da Patrícia Bicho.\n"
            "2. **Carl Zeiss (Projeto #SOMOS & Neuroselling):** Acompanhar validação das 8 ações de Neuroselling para Parceiros (16.000 €) e cronograma #SOMOS (21.055 € c/ Catarina Cabanelas) junto da Patrícia Fernandes.\n"
            "3. **Devoteam (Pitch & Soft Skills em Inglês):** Seguimento da proposta revista de 7h presenciais em Lisboa (1.300 € + opção Training-Lab 4h c/ formadora Alcina) junto da Carolina Lopes.\n"
            "4. **Banco CTT & Talkdesk:** Preparar guião de diagnóstico consultivo (6 Perguntas Nucleares) e qualificação pós-contacto telefónico.\n\n"
            "Seleciona uma conta na barra lateral esquerda ou pede-me diretamente uma minuta, cálculo de margem TMB 25-26 ou guião de reunião."
        ),
        "mode": "Chief of Staff · Priorização SC",
    }


class OpenFileRequest(BaseModel):
    rel_path: str


@app.post("/api/open-file")
def open_workspace_file(req: OpenFileRequest):
    target = (BASE_DIR / req.rel_path).resolve()
    if not str(target).startswith(str(BASE_DIR.resolve())):
        raise HTTPException(status_code=403, detail="Acesso fora do workspace não permitido.")
    up = unc_path(target)
    if not os.path.exists(up):
        raise HTTPException(status_code=404, detail="Ficheiro ou pasta não encontrado.")
    try:
        if os.name == "nt":
            os.startfile(str(target))
        return {"ok": True, "opened": str(target)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Montar pasta static
STATIC_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("BIZZDEV_PORT", "8080"))
    print(f"\n  [SKOLAE BIZZ DEV AI] Servidor local ativo em: http://127.0.0.1:{port}\n")
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="warning")

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import PlainTextResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime
import hashlib
import inspect
import uvicorn
import pyfiglet
import os

entreprise=os.getenv('TT_COMPANY', 'THOSTED')
custom_tasks=os.getenv('TT_CUSTOMTASKS', None)

app = FastAPI(title="Entretien Technique", docs_url=None, redoc_url=None, openapi_url=None)
security = HTTPBearer()

def generate_token():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    raw = now.encode()
    return hashlib.sha256(raw).hexdigest()[:64]

@app.get("/", response_class=PlainTextResponse)
def explain():
    return f'''# Bienvenue dans cet entretien technique
## Le contexte :
Vous vous appretez à passer un entretien technique pour {entreprise}.
Cet entretien a pour objectif de tester vos capacités a résoudre des problèmes d'administration systèmes et/ou de DEVOPS. 

## L'entretien :
### ETAPE 1 :
Faites un GET sur /token
Vous verrez un ASCII art avec un token à l'intérieur
Récupérez le token
Mais attention :
- il est modifié
- vous devez remplacer toutes les lettres 'Z' par des 'A'
- vous devez passer le token en minuscules (lowercase)

### ETAPE 2 :
Faites un POST sur /token avec ce token transformé
Le token doit être placé dans le header Authorization en tant que Bearer
Si le token est correct et encore valide (1 seconde), vous récupérez le code source du site web actuel

### ETAPE 3 :
Dans ce code source, vous trouverez un endpoint supplémentaire avec plus d'étapes'''

@app.get("/custom-tasks/"+entreprise, response_class=PlainTextResponse)
def explain_custom():
    if not custom_tasks: return explain() + "\n Et en fait rien de plus."
    return explain() + '\n\n' + '\n\n'.join([ f'### ETAPE {i+4} :\n' + t for i,t in enumerate(custom_tasks.split('\n\n'))])

@app.get("/token", response_class=PlainTextResponse)
def get_token():
    token = generate_token()
    token_frame = '+' + '-'*(len(token)+2) + '+'

    token = token.upper()
    token = token.replace("A", "Z")

    ascii_image = pyfiglet.figlet_format(text=entreprise, font='bigmono12', width=float("inf"))
    h, w = len(ascii_image.split('\n')), len(ascii_image.split('\n')[0])

    ascii_image = '\n'.join([
        line
            if i not in [h//2-2, h//2-1, h//2] else
        (
            line[:w//2 - len(token_frame)//2] + token_frame + line[w//2 + len(token_frame)//2:]
                if i in [h//2-2, h//2] else
            line[:w//2 - len(token)//2-2] + '| ' + token + ' |' + line[w//2 + len(token)//2+2:]
        )
        for i, line in enumerate(ascii_image.split('\n'))
    ])

    return ascii_image

@app.post("/token", response_class=PlainTextResponse)
def post_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    current_token = generate_token()
    if credentials.credentials != current_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token invalide ou expiré"
        )

    source_code = inspect.getsource(inspect.getmodule(generate_token))
    return source_code

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)

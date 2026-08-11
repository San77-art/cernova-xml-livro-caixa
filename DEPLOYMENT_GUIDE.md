# DEPLOYMENT GUIDE - PRODUÇÃO AWS

## Pré-requisitos

- AWS Account com permissões
- Terraform instalado
- PostgreSQL 18.3+
- Python 3.12+

## Passo 1: Setup Terraform

\\\ash
cd terraform
terraform init
terraform plan
terraform apply
\\\

## Passo 2: Environment Variables

Criar \.env\ em produção:

\\\
DATABASE_URL=postgresql://user:password@rds-endpoint:5432/cernova_rb
ENVIRONMENT=production
AWS_REGION=eu-north-1
\\\

## Passo 3: Deploy FastAPI

\\\ash
pip install -r requirements.txt
python -m app.main
\\\

## Passo 4: Testes

\\\ash
pytest tests/integration/test_endpoints.py
pytest tests/security/test_rls.py
\\\

## Passo 5: Monitoramento

- CloudWatch para logs
- RDS Enhanced Monitoring
- Application Performance Monitoring

## Rollback

\\\ash
git revert COMMIT_ID
terraform plan
terraform apply
\\\

## Suporte

Para issues de produção, verificar:
1. PostgreSQL connection
2. Environment variables
3. RLS policies ativas
4. Application logs


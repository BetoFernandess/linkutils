import pandas as pd
import json

def cria_tabela_vendas(servidor):
    json_tabela = {}

    tabela = cria_base_tabela(sevidor)
    
    tabela_financeiro = cria_dados_finaceiros(servidor)


    for cupom,data,hora,caixa,tipo_cupom,valor_bruto,desconto,impostos,custo,valor_total,lucro in zip(tabela["Cupom"],tabela["Data"],tabela["Hora"],tabela["Caixa"],tabela["Tipo"], tabela_financeiro["Valor Bruto"],tabela_financeiro["Desconto"], tabela_financeiro["Impostos"],tabela_financeiro["Custo"], tabela_financeiro["Valor Total"],tabela_financeiro["Lucro"]):
        coluna= {}
    
        coluna["Cupom"] = cupom
        coluna["Data"] = '0{}/0{}/{}'.format(data.day, data.month, data.year)
        coluna["Hora"] = str(hora)
        coluna["Caixa"] = caixa
        coluna["Tipo"] = {True: "Sem Nota Fiscal" ,False:tipo_cupom}[tipo_cupom == ""] 

        coluna["Valor Bruto"]= "R${: .2f}".format(valor_bruto).replace('.', ',')
        coluna["Desconto"] = "R${: .2f}".format(desconto).replace('.', ',')
        coluna["Impostos"] = "R${: .2f}".format(impostos).replace('.', ',')
        coluna["Custo"] = "R${: .2f}".format(custo).replace('.', ',')
        coluna["Valor Total"] = "R${: .2f}".format(valor_total).replace('.', ',')
        coluna["Lucro"] = "R${: .2f}".format(lucro).replace('.', ',')

        json_tabela.append(coluna)
    
    return json.dumps(json_tabela)


def cria_dados_finaceiros(servidor):

    financeiro = pd.read_sql_query("SELECT `NUMERO_CUPOM` as `Cupom`, `VALOR_TOTAL`, `DESCONTO_PEDIDO`, `DESCONTO_ITEM`, `CUSTO_TOTAL`, `ST`, `IPI` FROM `faturamento_caixa` WHERE YEAR(`faturamento_caixa`.`DATA`) = 2021 and MONTH(`faturamento_caixa`.`DATA`) = 1 ORDER BY `faturamento_caixa`.`NUMERO_CUPOM`",servidor)

    tabela_financeiro = {}

    tabela_financeiro["Valor Bruto"]= financeiro.groupby("Cupom")["VALOR_TOTAL"].sum()
    tabela_financeiro["Desconto"]= financeiro.groupby("Cupom")["DESCONTO_PEDIDO"].sum() + financeiro.groupby("Cupom")["DESCONTO_ITEM"].sum()
    tabela_financeiro["Impostos"]= financeiro.groupby("Cupom")['ST'].sum() + financeiro.groupby("Cupom")['IPI'].sum()
    tabela_financeiro["Custo"]= financeiro.groupby("Cupom")['CUSTO_TOTAL'].sum()
    tabela_financeiro["Valor Total"]= tabela_financeiro["Valor Bruto"] - tabela_financeiro["Desconto"] - tabela_financeiro["Impostos"]
    tabela_financeiro["Lucro"]=  tabela_financeiro["Valor Total"] - tabela_financeiro["Custo"]

    return tabela_financeiro

def cria_base_tabela(servidor):
    return pd.read_sql_query("SELECT DISTINCT `Data`, `Hora`, `NUMERO_CUPOM` as `Cupom`, `Loja`, `Caixa`,`Tipo` FROM `faturamento_caixa` WHERE YEAR(`faturamento_caixa`.`DATA`) = 2021 and MONTH(`faturamento_caixa`.`DATA`) = 1 ORDER BY `faturamento_caixa`.`NUMERO_CUPOM`",servidor).drop_duplicates(subset="Cupom")

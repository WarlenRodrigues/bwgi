import csv
from pathlib import Path
from pprint import pprint
from datetime import datetime

def reconcile_accounts(account_a, account_b):

    # Convert dates
    def parse_date(date_str):
        return datetime.strptime(date_str, "%Y-%m-%d")

    def is_matching(transaction1, transaction2):
        # Match fields and valid date interval
        return (
            transaction1[1:] == transaction2[1:] and
            abs((parse_date(transaction1[0]) - parse_date(transaction2[0])).days) <= 1
        )

    # Result lists
    res_a = []
    res_b = []

    # Control lists
    # Used this list to avoid .remove() wich is an O(m) operation
    used_in_b = [False] * len(account_b)

    # Sort second list to ensure getting the older transaction when there are multiple options to concile
    account_b.sort(key=lambda x: x[0])

    # For each transaction in account_a
    for t1 in account_a:
        t1_res = t1
        for i, t2 in enumerate(account_b):
            if not used_in_b[i] and is_matching(t1, t2):
                t2_res = t2
                t1_res.append("FOUND")
                t2_res.append("FOUND")
                res_b.append(t2_res)

                # Prevent next iterations to check this element again
                used_in_b[i] = True
                break
        else:
            # If t1 does not match to any t2, set MISSING prop
            t1_res.append("MISSING")
        res_a.append(t1_res)
            
    # Adding MISSING prop to every ramaining transaction in account_b        
    for i, flag in enumerate(used_in_b):
        if not flag:
            t2_res = account_b[i]
            t2_res.append("MISSING")
            res_b.append(t2_res)
        
    return res_a, res_b

transactions1 = list(csv.reader(Path('transactions1.csv').open()))
transactions2 = list(csv.reader(Path('transactions2.csv').open()))
out1, out2 = reconcile_accounts(transactions1, transactions2)
pprint(out1)
pprint(out2)

'''
 Construção:
 
 Comecei com um pseudo-código para organizar meu raciocínio, onde encontrei, além das comparações básicas, a necessidade de ordenação da account_b para garantir a condição de prioridade de data e, depois, a necessidade de não verificação do mesmo item em account_b duas vezes. Depois evolui para um código bem legível e bem simples, para fazer funcinar. O passo seguinte foi buscar por melhorias no código em relação a organização e limpeza e, por fim, melhorias de desempenho (onde optei por trabalhar com a lista auxiliar ao invés de usar o método de remoção)

 Complexidade:

 O código possui uma complexidade de tempo de O(nm) + O(mlog(m)), sendo esse último componente necessário para garantir que a transação A será conciliada com a Transação B mais antiga dentro do intervalo permitido

 Evitar o uso do remove() com a lista auxiliar garantiu que não caíssemos num cenário de O(nm2) visto que o método remove() possui complexidade O(m) por operação de conciliação bem sucedida.
 
 Em relação à memória, o código possui uma complexidade O(n+m) visto que as listas de suporte e resultado possuem, no pior caso, o tamanho das listas originalmente recebidas.

 Pode ser melhorado com uso de dicionário *Estudar Implementação* 
 
'''
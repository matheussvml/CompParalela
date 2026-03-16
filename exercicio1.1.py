import math
import os
import plotly.graph_objects as go

def disponibilidade(n, k, p):
    """
    Calcula a disponibilidade de um serviço replicado usando a distribuição binomial.
    
    A(n,k,p) = soma de i=k até n de (C(n,i) * p^i * (1-p)^(n-i))
    
    :param n: número total de servidores (n > 0)
    :param k: número mínimo de servidores disponíveis necessários (0 < k <= n)
    :param p: probabilidade de cada servidor estar disponível (0 <= p <= 1)
    :return: A disponibilidade do serviço
    """
    if not (0 <= p <= 1):
        raise ValueError("A probabilidade 'p' deve estar entre 0 e 1.")
    if not (0 < k <= n):
        raise ValueError("'k' deve ser maior que 0 e menor ou igual a 'n'.")
        
    soma = 0
    for i in range(k, n + 1):
        combinacao = math.comb(n, i)
        termo = combinacao * (p ** i) * ((1 - p) ** (n - i))
        soma += termo
        
    return soma


def consulta(n, p):
    """
    Calcula  a disponibilidade para o caso extremo de consulta (leitura), onde k = 1.
    
    A = 1 - (1-p)^n
    """
    if not (0 <= p <= 1):
        raise ValueError("A probabilidade 'p' deve estar entre 0 e 1.")
    if n <= 0:
        raise ValueError("'n' deve ser maior que 0.")
        
    return 1 - ((1 - p) ** n)


def atualizacao(n, p):
    """
    Calcula a disponibilidade para o caso extremo de atualização (escrita), onde k = n.
    
    A = p^n
    """
    if not (0 <= p <= 1):
        raise ValueError("A probabilidade 'p' deve estar entre 0 e 1.")
    if n <= 0:
        raise ValueError("'n' deve ser maior que 0.")
        
    return p ** n


if __name__ == "__main__":
    print("--- Exemplos de Uso ---")
    n_servidores = 5
    p_disponivel = 0.9
    
    print(f"Número total de servidores (n): {n_servidores}")
    print(f"Probabilidade de disponibilidade de cada servidor (p): {p_disponivel * 100}%\n")
    
    # Exemplo genérico: k = 3
    k_minimo = 3
    disp_geral = disponibilidade(n_servidores, k_minimo, p_disponivel)
    print(f"1. Disponibilidade genérica (k mínimo = {k_minimo}): {disp_geral:.6f} ({disp_geral * 100:.4f}%)")
    
    # Exemplo consulta: k = 1
    disp_cons = consulta(n_servidores, p_disponivel)
    print(f"2. Disponibilidade para consulta (k = 1): {disp_cons:.6f} ({disp_cons * 100:.4f}%)")
    
    # Verifica equivalência da função geral para k = 1
    disp_geral_cons = disponibilidade(n_servidores, 1, p_disponivel)
    print(f"   (Verificação usando a função genérica): {disp_geral_cons:.6f}")
    
    # Exemplo atualização: k = n
    disp_atual = atualizacao(n_servidores, p_disponivel)
    print(f"3. Disponibilidade para atualização (k = {n_servidores}): {disp_atual:.6f} ({disp_atual * 100:.4f}%)")
    
    # Verifica equivalência da função geral para k = n
    disp_geral_atual = disponibilidade(n_servidores, n_servidores, p_disponivel)
    print(f"   (Verificação usando a função genérica): {disp_geral_atual:.6f}")

    print("\nGerando gráfico comparativo para o Exercício 1.1...")
    
    # Gerar dados para o gráfico de 1 a 10 servidores
    eixo_x_n = list(range(1, 11))
    
    y_consulta = [consulta(n, p_disponivel) for n in eixo_x_n]
    y_atualizacao = [atualizacao(n, p_disponivel) for n in eixo_x_n]
    
    # Para o caso genérico k=majority (maioria simples)
    y_maioria = [disponibilidade(n, (n // 2) + 1, p_disponivel) for n in eixo_x_n]

    fig = go.Figure()

    # Curva de Consulta (k=1)
    fig.add_trace(go.Scatter(
        x=eixo_x_n, y=y_consulta,
        mode='lines+markers', name='Consulta (k=1)',
        line=dict(color='#27ae60', width=3),
        marker=dict(symbol='circle', size=8)
    ))

    # Curva de Maioria Genérica (k=maioria)
    fig.add_trace(go.Scatter(
        x=eixo_x_n, y=y_maioria,
        mode='lines+markers', name='Maioria (k=⌈n/2⌉)',
        line=dict(color='#f39c12', width=3),
        marker=dict(symbol='square', size=8)
    ))

    # Curva de Atualização (k=n)
    fig.add_trace(go.Scatter(
        x=eixo_x_n, y=y_atualizacao,
        mode='lines+markers', name='Atualização (k=n)',
        line=dict(color='#e74c3c', width=3),
        marker=dict(symbol='diamond', size=8)
    ))

    fig.update_layout(
        title=f'<b>Disponibilidade do Serviço Replicado vs N</b><br>(Probabilidade do servidor p = {p_disponivel})',
        xaxis_title='Número Total de Servidores (n)',
        yaxis_title='Disponibilidade do Serviço (A)',
        yaxis=dict(range=[0, 1.05]),
        xaxis=dict(tickmode='linear', tick0=1, dtick=1),
        template='plotly_white',
        legend=dict(yanchor="bottom", y=0.05, xanchor="right", x=0.95),
        hovermode="x unified"
    )

    caminho_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_grafico = os.path.join(caminho_atual, "grafico_exercicio1.1.png")

    try:
        fig.write_image(caminho_grafico, scale=2)
        print(f"Gráfico comparativo salvo com sucesso em:\n{caminho_grafico}")
    except ValueError:
        caminho_grafico_html = os.path.join(caminho_atual, "grafico_exercicio1.1.html")
        fig.write_html(caminho_grafico_html)
        print(f"O gráfico foi salvo como HTML interativo (não há kaleido para exportação em PNG):\n{caminho_grafico_html}")
    except Exception as e:
        print(f"Ocorreu um erro ao salvar o gráfico: {e}")
        try:
            caminho_grafico_html = os.path.join(caminho_atual, "grafico_exercicio1.1.html")
            fig.write_html(caminho_grafico_html)
            print(f"Fallback para HTML interativo:\n{caminho_grafico_html}")
        except:
            pass

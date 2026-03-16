import plotly.graph_objects as go
import os

def calcular_n_minimo(p, disponibilidade_alvo):

    """
    Calcula o número mínimo de servidores (n) para atingir uma disponibilidade alvo
    considerando operação de leitura (k=1).
    A fórmula para k=1 é: A = 1 - (1-p)^n
    """
    n = 1
    while True:
        # Fómula para consulta (k=1)
        disponibilidade_atual = 1 - ((1 - p) ** n)
        if disponibilidade_atual >= disponibilidade_alvo:
            return n, disponibilidade_atual
        n += 1

def principal():
    # Parâmetros dados no exercício
    p = 0.5
    k = 1 # Operação de leitura, o que resulta na fórmula de A = 1 - (1-p)^n
    
    # Alvos de disponibilidade exigidos
    alvos = [
        0.9,       # 90%
        0.99,      # 99%
        0.999,     # 99.9%
        0.9999,    # 99.99%
        0.99999,   # 99.999%
        0.999999   # 99.9999%
    ]
    
    # Listas para visualização e geração de gráficos
    resultados_n = []
    resultados_disp = []
    
    print(f"--- Resultados de Disponibilidade (p = {p}, k = {k}) ---")
    print(f"{'Alvo':<10} | {'Servidores (n)':<15} | {'Disponibilidade Atingida'}")
    print("-" * 60)
    
    for alvo in alvos:
        n, disp_real = calcular_n_minimo(p, alvo)
        
        resultados_n.append(n)
        resultados_disp.append(disp_real)
        
        # Formatando para exibição terminal
        formato_alvo = f"{alvo * 100:g}%"
        formato_real = f"{disp_real * 100:.6f}%"
        print(f"{formato_alvo:<10} | {n:<15} | {formato_real}")

    print("\nGerando gráfico de disponibilidade...")
    
    # Gerando dados para cobrir o intervalo de n = 1 até o máximo N listado + 2 (para visualização)
    n_maximo = max(resultados_n)
    
    eixo_x_n = list(range(1, n_maximo + 3))
    eixo_y_disp = [1 - ((1 - p) ** n) for n in eixo_x_n]
    
    # Configurando e gerando o gráfico com plotly
    fig = go.Figure()
    
    # Curva contínua de disponibilidade
    fig.add_trace(go.Scatter(
        x=eixo_x_n, 
        y=eixo_y_disp,
        mode='lines+markers',
        name='Curva de Disponibilidade (A)',
        line=dict(color='#2c3e50'),
        marker=dict(size=6)
    ))
    
    # Pontos de meta (vermelho) sobre a curva
    fig.add_trace(go.Scatter(
        x=resultados_n,
        y=resultados_disp,
        mode='markers+text',
        name='N mínimo para cada meta',
        marker=dict(color='#e74c3c', size=12),
        text=[f'{alvo_disp*100:g}% (n={n})' for n, alvo_disp in zip(resultados_n, alvos)],
        textposition="top left"
    ))
    
    # Títulos e labels
    fig.update_layout(
        title='<b>Disponibilidade vs Número de Servidores</b><br>(p = 0.5, k = 1)',
        xaxis_title='Número Total de Servidores (n)',
        yaxis_title='Disponibilidade do Serviço (A)',
        yaxis=dict(range=[0, 1.05]),
        xaxis=dict(tickmode='linear', tick0=1, dtick=1), # Força exibir cada N no X
        legend=dict(
            yanchor="bottom",
            y=0.05,
            xanchor="right",
            x=0.95
        ),
        template='plotly_white'
    )
    
    # Caminho do diretório do script atual garante que seja salvo junto com os exercícios
    caminho_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_grafico = os.path.join(caminho_atual, "grafico_disponibilidade.png")
    
    # Salvar diagrama
    try:
        fig.write_image(caminho_grafico, scale=2)
        print(f"Gráfico salvo com sucesso em:\n{caminho_grafico}")
    except ValueError as e:
        print("Erro ao tentar salvar versão em PNG. Pode ser necessário instalar o pacote 'kaleido'.")
        print("Dica: pip install -U kaleido")
        # Fallback para salvar como HTML interativo
        caminho_grafico_html = os.path.join(caminho_atual, "grafico_disponibilidade.html")
        fig.write_html(caminho_grafico_html)
        print(f"O gráfico foi salvo como HTML interativo em vez disso:\n{caminho_grafico_html}")
    except Exception as e:
        print(f"Ocorreu um erro ao salvar o gráfico: {e}")
        # Tenta fallback para HTML caso seja outro erro de dependência na exportação estática
        try:
            caminho_grafico_html = os.path.join(caminho_atual, "grafico_disponibilidade.html")
            fig.write_html(caminho_grafico_html)
            print(f"O gráfico foi salvo como HTML interativo:\n{caminho_grafico_html}")
        except:
            pass

if __name__ == "__main__":
    principal()

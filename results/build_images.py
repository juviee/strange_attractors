import matplotlib.pyplot as plt
vec_src = list()
dataX = list()
dataY = list()
with open('../data', 'r') as f:
    while True:
        line = f.readline()
        if line == '':
            break
        dataY.append(float(f))


fig, m_graph = plt.subplots (1)
m_graph.plot (dataX, dataY, ls = 'None', marker = 'x')
m_graph.grid (True)
m_graph.set_xlim(1,16)
fig_name = "Dimension asymptotics"
m_graph.set_title (fig_name)
fig.set_size_inches( 5, 5)
fig.tight_layout ()
fig.savefig (fig_name + ".png")

import io, base64, urllib, matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt


def plot_to_png(data):
    plt.clf()
    for key, value in data.items():
        plt.plot(value, label=key)
    buf = io.BytesIO()
    plt.legend()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return 'data:image/png;base64,' + urllib.quote(base64.b64encode(buf.read()))


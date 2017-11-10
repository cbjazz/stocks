"""
Simple demo of a horizontal bar chart.
"""
import matplotlib.pyplot as plt
plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins


def d3exam():
	# Example data
	people = ('Tom', 'Dick', 'Harry', 'Slim', 'Jim')
	y_pos = np.arange(len(people))
	performance = 3 + 10 * np.random.rand(len(people))
	error = np.random.rand(len(people))

	fig, ax = plt.subplots()

	ax.barh(y_pos, performance, xerr=error, align='center', alpha=0.4)

	plt.yticks(y_pos, people)
	plt.xlabel('Performance')
	plt.title('How fast do you want to go today?')

	return  mpld3.fig_to_html(fig)

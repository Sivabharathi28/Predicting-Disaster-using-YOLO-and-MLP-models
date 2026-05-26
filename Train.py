import pickle
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import animation
from sklearn.preprocessing import StandardScaler
import webbrowser

data = pd.read_csv("earth/balanced_earthquake_dataset.csv")
# Fill missing values with column means
data = data.fillna(data.mean())

print(data.columns)
print(data.head())

lengths = data["Date"].str.len()
print(lengths.value_counts())

data.fillna(value=0, inplace=True)
plt.figure(figsize=(10,5))
sns.countplot(x="Type", data=data)
plt.title ("Explosion details")
plt.xlabel("Type of explosion")
plt.ylabel("count of explosion type ")
plt.show()

plt.hist(data['Magnitude'], bins=20)
plt.xlabel('Magnitude')
plt.ylabel('Count')
plt.title('Histogram of Earthquake Magnitudes')
plt.show()

import matplotlib.pyplot as plt

# Create scatter plot
fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(data['Longitude'], data['Latitude'], c=data['Magnitude'], cmap='viridis', alpha=0.5)

# Set plot properties
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('Earthquake Occurrences')
fig.colorbar(scatter, label='Magnitude')

# Show plot
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
heatmap = sns.histplot(data=data, x='Longitude', y='Latitude', bins=50, cmap='YlOrRd', cbar=True, ax=ax)

# Set plot properties
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('Earthquake Occurrences')

# Show plot
plt.show()

import matplotlib.pyplot as plt



# Create heat map
fig, ax = plt.subplots(figsize=(10, 6))
heat_map = sns.kdeplot(x=data['Longitude'], y=data['Latitude'], cmap='YlGnBu', fill=True, thresh=False)

# Set plot properties
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('Earthquake Density and Distribution')

# Show plot
plt.show()

plt.scatter(data['Depth'], data['Magnitude'], color='blue')
plt.title('Earthquake Depth vs. Magnitude')
plt.xlabel('Depth (km)')
plt.ylabel('Magnitude')
plt.show()

import seaborn as sns

# plot violin plot of earthquake magnitudes
sns.violinplot(x=data['Magnitude'])
plt.title('Distribution of Earthquake Magnitudes')
plt.xlabel('Magnitude')
plt.show()

import folium
from folium.plugins import HeatMap

# create a map centered on the average latitude and longitude of the earthquake data
map_center = [data.Latitude.mean(), data.Longitude.mean()]
m = folium.Map(location=map_center, zoom_start=2)

# create a heatmap layer based on the earthquake data
heat_data = data[['Latitude', 'Longitude']].values.tolist()
HeatMap(heat_data, name='Heatmap', control=False).add_to(m)

# add a layer control to the map
folium.LayerControl().add_to(m)

# display the map
m.save('sample.html')

# specify the path to the HTML file
html_file = 'sample.html'

# open the HTML file in a Chrome window
webbrowser.open_new(html_file)


# generate some dummy earthquake data
magnitude = np.random.randint(1, 6, size=(10, 10))
depth = np.random.randint(1, 11, size=(10, 10))
x = np.arange(0, 10)
y = np.arange(0, 10)

# calculate the gradient of the data
dy, dx = np.gradient(depth)

# plot the streamplot
fig, ax = plt.subplots(figsize=(8, 6))
ax.streamplot(x, y, dx, dy, density=0.8, color=magnitude, cmap='YlGnBu')
ax.set_title('Earthquake Streamplot')
ax.set_xlabel('X')
ax.set_ylabel('Y')
plt.show()

plt.scatter(data['Longitude'], data['Latitude'], c=data['Magnitude'], cmap='inferno')

# Set axis labels and title
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Seismicity Map')

# Add colorbar
cbar = plt.colorbar()
cbar.set_label('Magnitude')

# Display the plot
plt.show()

from mpl_toolkits.basemap import Basemap

m = Basemap(projection='mill',llcrnrlat=-80,urcrnrlat=80, llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')

longitudes = data["Longitude"].tolist()
latitudes = data["Latitude"].tolist()
#m = Basemap(width=12000000,height=9000000,projection='lcc',
            #resolution=None,lat_1=80.,lat_2=55,lat_0=80,lon_0=-107.)
x,y = m(longitudes,latitudes)

fig = plt.figure(figsize=(12,10))
plt.title("All affected areas")
m.plot(x, y, "o", markersize = 2, color = 'blue')
m.drawcoastlines()
m.fillcontinents(color='coral',lake_color='aqua')
m.drawmapboundary()
m.drawcountries()
plt.show()

data.label = data.Type.map({'Earthquake':0,
                            'Explosion' :1,
                            'Nuclear Explosion':2})




from sklearn.model_selection import train_test_split
X = data[['Latitude', 'Longitude', 'Depth', 'Magnitude']]
y = data['Type']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)
print(X_train, X_test, y_train, y_test)

from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
classifier = MLPClassifier(random_state=0)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)
print(classification_report(y_test, y_pred))
print("Accuracy on training set: {:.2f}".format(classifier.score(X_train, y_train)))
print("Accuracy on test set: {:.3f}".format(classifier.score(X_test, y_test)))

# Creating a pickle file for the classifier
filename = 'earthquakeprediction.pkl'
pickle.dump(classifier, open(filename, 'wb'))

classifier = pickle.load(open(filename, 'rb'))


data = np.array([[10.790483,78.704674,9,10]])
my_prediction = classifier.predict(data)

warnings.filterwarnings("ignore", category=DeprecationWarning)
print(my_prediction)

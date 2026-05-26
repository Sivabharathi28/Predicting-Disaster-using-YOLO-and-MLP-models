import pickle
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import webbrowser
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Load data
data = pd.read_csv("earth/database.csv")

# Fill missing values with column means
data = data.fillna(data.mean(numeric_only=True))

print(data.columns)
print(data.head())

# Checking Date column lengths
if "Date" in data.columns:
    lengths = data["Date"].astype(str).str.len()
    print(lengths.value_counts())

data.fillna(value=0, inplace=True)

# Plotting explosion details
plt.figure(figsize=(10, 5))
sns.countplot(x="Type", data=data)
plt.title("Explosion details")
plt.xlabel("Type of explosion")
plt.ylabel("Count of explosion type")
plt.xticks(rotation=45)
plt.show()

# Histogram of Earthquake Magnitudes
plt.hist(data['Magnitude'], bins=20, edgecolor='black')
plt.xlabel('Magnitude')
plt.ylabel('Count')
plt.title('Histogram of Earthquake Magnitudes')
plt.show()

# Scatter plot of Earthquakes
fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(data['Longitude'], data['Latitude'], c=data['Magnitude'], cmap='viridis', alpha=0.5)
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('Earthquake Occurrences')
fig.colorbar(scatter, label='Magnitude')
plt.show()

# Heatmap using histplot
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(data=data, x='Longitude', y='Latitude', bins=50, cmap='YlOrRd', cbar=True, ax=ax)
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('Earthquake Occurrences')
plt.show()

# KDE Plot (Updated for Python 3.10)
fig, ax = plt.subplots(figsize=(10, 6))
sns.kdeplot(x=data['Longitude'], y=data['Latitude'], cmap='YlGnBu', fill=True, levels=100)
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('Earthquake Density and Distribution')
plt.show()

# Depth vs. Magnitude Scatter plot
plt.scatter(data['Depth'], data['Magnitude'], color='blue', alpha=0.5)
plt.title('Earthquake Depth vs. Magnitude')
plt.xlabel('Depth (km)')
plt.ylabel('Magnitude')
plt.show()

# Violin Plot of Earthquake Magnitudes
sns.violinplot(x=data['Magnitude'])
plt.title('Distribution of Earthquake Magnitudes')
plt.xlabel('Magnitude')
plt.show()

# Folium Heatmap
import folium
from folium.plugins import HeatMap

map_center = [data.Latitude.mean(), data.Longitude.mean()]
m = folium.Map(location=map_center, zoom_start=2)
heat_data = data[['Latitude', 'Longitude']].dropna().values.tolist()
HeatMap(heat_data, name='Heatmap', control=False).add_to(m)
folium.LayerControl().add_to(m)

m.save('sample.html')
webbrowser.open_new('sample.html')

# Generate dummy earthquake data for Streamplot
magnitude = np.random.randint(1, 6, size=(10, 10))
depth = np.random.randint(1, 11, size=(10, 10))
x = np.arange(0, 10)
y = np.arange(0, 10)

dy, dx = np.gradient(depth)

fig, ax = plt.subplots(figsize=(8, 6))
ax.streamplot(x, y, dx, dy, density=0.8, color=magnitude, cmap='YlGnBu')
ax.set_title('Earthquake Streamplot')
ax.set_xlabel('X')
ax.set_ylabel('Y')
plt.show()

# Seismicity Map
plt.scatter(data['Longitude'], data['Latitude'], c=data['Magnitude'], cmap='inferno', alpha=0.5)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Seismicity Map')
cbar = plt.colorbar()
cbar.set_label('Magnitude')
plt.show()

# Mapping (Optional: Use Cartopy Instead of Basemap)
try:
    from mpl_toolkits.basemap import Basemap

    m = Basemap(projection='mill', llcrnrlat=-80, urcrnrlat=80,
                llcrnrlon=-180, urcrnrlon=180, lat_ts=20, resolution='c')

    longitudes = data["Longitude"].tolist()
    latitudes = data["Latitude"].tolist()
    x, y = m(longitudes, latitudes)

    fig = plt.figure(figsize=(12, 10))
    plt.title("All Affected Areas")
    m.plot(x, y, "o", markersize=2, color='blue')
    m.drawcoastlines()
    m.fillcontinents(color='coral', lake_color='aqua')
    m.drawmapboundary()
    m.drawcountries()
    plt.show()
except ImportError:
    print("Basemap not installed. Skipping world map plot.")

# Encoding categorical labels
data['label'] = data['Type'].map({'Earthquake': 0, 'Explosion': 1, 'Nuclear Explosion': 2})

# Model Training
X = data[['Latitude', 'Longitude', 'Depth', 'Magnitude']]
y = data['label'].dropna()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)

classifier = MLPClassifier(hidden_layer_sizes=(100,), max_iter=500, random_state=0)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)
print(classification_report(y_test, y_pred))
print("Accuracy on training set: {:.2f}".format(classifier.score(X_train, y_train)))
print("Accuracy on test set: {:.3f}".format(classifier.score(X_test, y_test)))

# Save Model
filename = 'earthquakeprediction.pkl'
pickle.dump(classifier, open(filename, 'wb'))

# Load and Predict
classifier = pickle.load(open(filename, 'rb'))
warnings.filterwarnings("ignore", category=DeprecationWarning)

test_data = np.array([[10.790483, 78.704674, 9, 10]])
my_prediction = classifier.predict(test_data)
print(my_prediction)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


def count_word(filename):
    text = open(filename).read()
    for char in '@#!%:;&-.,\n':
        text = text.replace(char, ' ')
    text = text.lower()
    word_list = text.split()
    d = {}

    for word in word_list:
        d[word] = d.get(word, 0) + 1

    return d


documents = open("captions.txt", "r")
count = count_word("captions.txt")

vector = TfidfVectorizer(stop_words='english')
X = vector.fit_transform(documents)

n_clusters = 5
model = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=100, n_init=1)
model.fit(X)

print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vector.get_feature_names()
text_file = open("Output.txt", "w")
for i in range(n_clusters):
    print("Cluster %d:" % i),
    text_file.write("Cluster %d:\n" % i)
    for j in order_centroids[i, :15]:
        print(' %s %d' % (terms[j], count[terms[j]]))
        text_file.write(' %s %d\n' % (terms[j], count[terms[j]], ))

text_file.close()


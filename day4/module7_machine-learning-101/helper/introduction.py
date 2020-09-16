import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds
from skbio import OrdinationResults
from skbio.stats.composition import clr
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

plt.style.use("ggplot")

def regression_example(table, x_label='Blue', y_label='Red'):

    """
    from https://scikit-learn.org/stable/auto_examples/linear_model/plot_ols.html
    """

    figure = plt.figure(figsize=(5, 5))
    ax = plt.subplot(1, 1, 1)

    X = table[x_label].values.reshape(-1,1)
    y = table[y_label].values

    split_ = X.shape[0]//2
    X_train, y_train = X[:-split_], y[:-split_]
    X_test, y_test = X[split_:], y[split_:]

    # Create linear regression object
    regr = linear_model.LinearRegression()

    # Train the model using the training sets
    regr.fit(X_train, y_train)

    # Make predictions using the testing set
    y_pred = regr.predict(X_test)

    # The coefficients
    print('Coefficients: \n', regr.coef_)
    # The mean squared error
    print('Mean squared error: %.2f'
        % mean_squared_error(y_test, y_pred))
    # The coefficient of determination: 1 is perfect prediction
    print('Coefficient of determination: %.2f'
        % r2_score(y_test, y_pred))

    # Plot outputs
    sns.scatterplot(x=x_label, y=y_label, hue=y_label, palette='Reds',
                    data=table,  color='black', ax=ax)
    ax.plot(X_test, y_pred, color='black', linewidth=2)
    ax.set_xticks(())
    ax.set_yticks(())

    return ax

def classifier_example(table, mf, classcol='more_red'):

    """
    code from https://scikit-learn.org/stable/auto_examples/classification/plot_classifier_comparison.html
    """

    h = .02  # step size in the mesh

    names = ["Nearest Neighbors", "Linear SVM", "RBF SVM", "Gaussian Process",
            "Decision Tree", "Random Forest", "Neural Net", "AdaBoost",
            "Naive Bayes", "QDA"]

    classifiers = [
        KNeighborsClassifier(3),
        SVC(kernel="linear", C=0.025),
        SVC(gamma=2, C=1),
        GaussianProcessClassifier(1.0 * RBF(1.0)),
        DecisionTreeClassifier(max_depth=5),
        RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
        MLPClassifier(alpha=1, max_iter=1000),
        AdaBoostClassifier(),
        GaussianNB(),
        QuadraticDiscriminantAnalysis()]

    # Perform Aitchison PCA
    ordination = apca(table.T.astype(float))
    X = ordination.samples.values
    y = mf[classcol].values

    #rng = np.random.RandomState(2)
    #X += 2 * rng.uniform(size=X.shape)
    linearly_separable = (X, y)

    datasets = [linearly_separable]

    figure = plt.figure(figsize=(27, 3))
    i = 1
    # iterate over datasets
    for ds_cnt, ds in enumerate(datasets):
        # preprocess dataset, split into training and test part
        X, y = ds
        X = StandardScaler().fit_transform(X)
        X_train, X_test, y_train, y_test = \
            train_test_split(X, y, test_size=.5, random_state=42)

        x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
        y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                            np.arange(y_min, y_max, h))

        # just plot the dataset first
        cm = plt.cm.RdBu
        cm_bright = ListedColormap(['#FF0000', '#0000FF'])
        ax = plt.subplot(len(datasets), len(classifiers) + 1, i)
        if ds_cnt == 0:
            ax.set_title("Input data")
        # Plot the training points
        ax.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=cm_bright,
                edgecolors='k')
        # Plot the testing points
        ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=cm_bright, alpha=0.6,
                edgecolors='k')
        ax.set_xlim(xx.min(), xx.max())
        ax.set_ylim(yy.min(), yy.max())
        ax.set_xticks(())
        ax.set_yticks(())
        i += 1

        # iterate over classifiers
        for name, clf in zip(names, classifiers):
            ax = plt.subplot(len(datasets), len(classifiers) + 1, i)
            clf.fit(X_train, y_train)
            score = clf.score(X_test, y_test)

            # Plot the decision boundary. For that, we will assign a color to each
            # point in the mesh [x_min, x_max]x[y_min, y_max].
            if hasattr(clf, "decision_function"):
                Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
            else:
                Z = clf.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]

            # Put the result into a color plot
            Z = Z.reshape(xx.shape)
            ax.contourf(xx, yy, Z, cmap=cm, alpha=.8)

            # Plot the training points
            ax.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=cm_bright,
                    edgecolors='k')
            # Plot the testing points
            ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=cm_bright,
                    edgecolors='k', alpha=0.6)

            ax.set_xlim(xx.min(), xx.max())
            ax.set_ylim(yy.min(), yy.max())
            ax.set_xticks(())
            ax.set_yticks(())
            if ds_cnt == 0:
                ax.set_title(name, fontsize=18)
            ax.text(xx.max() - .3, yy.min() + .3, ('%.2f' % score).lstrip('0'),
                    size=18, horizontalalignment='right')
            i += 1

    plt.tight_layout()
    return ax


def apca(df):
    """Performs Aitchison PCA on a feature table.
    Parameters
    ----------
        df: pd.DataFrame
            A numeric DataFrame whose rows are "features" and whose columns are
            "samples."
    Returns
    -------
        A 3-tuple (U, p, V) where:
            U: pd.DataFrame
                Feature loadings.
            p: pd.DataFrame
                Proportions of variance explained.
            V: pd.DataFrame
                Sample loadings.
    """
    # do A-PCA
    U, s, V = svds(clr(df), k=2)
    V = V.T
    # reverse (see SVDs docs)
    U = np.flip(U, axis=1)
    V = np.flip(V, axis=1)
    s = s[::-1]

    # Rename columns; we use "Axis 1", etc. to be consistent with the Qurro
    # interface
    pcs = min(V.shape)
    cols = ["Axis {}".format(pc+1) for pc in range(pcs)]

    # Make DataFrames from the feature (U) and sample (V) loadings
    U = pd.DataFrame(U[:, :pcs], df.index, cols)
    V = pd.DataFrame(V[:, :pcs], df.columns, cols)

    # For clarity, rename top-left cell in both loading DataFrames
    U.index.name = "FeatureID"
    V.index.name = "SampleID"

    # get prop. var. explained
    p = s**2 / np.sum(s**2)
    p = pd.Series(p.T, index=cols)

    # format eigenvalues in a way that OrdinationResults expects
    eigvals = pd.Series(s.T, index=cols)

    return OrdinationResults(
        "apca",
        "Aitchison PCA",
        eigvals,
        samples=V,
        features=U,
        proportion_explained=p
    )

def draw_painting_biplot(ordination, axis_1, axis_2):
    """Draws a biplot using Seaborn and Matplotlib.
    Parameters
    ----------
        ordination: skbio.OrdinationResults
            Biplot ordination created from apca() above.
        axis_1: str
            Name of the first Axis to draw in the biplot.
        axis_2: str
            Name of the second Axis to draw in the biplot.
    """

    fig, ax = plt.subplots(1,1,figsize=(5,5))

    V = ordination.samples
    U = ordination.features
    p = ordination.proportion_explained

    # Draw points using a Seaborn scatterplot
    sns.scatterplot(
        x=axis_1, y=axis_2, data=V, s = 100, alpha=.25, color="#000000", ax=ax
    )
    # add dot annotation
    for i in V.index:
        ax.text(V.loc[i, axis_1], V.loc[i, axis_2], str(i), zorder=-1)

    # add arrows
    acmap = {"Black":"#000000", "White":"#ffffff",
             "Blue":"#377eb8", "Red":"#e41a1c",
             "Yellow":"#ffff33", "Other":"#999999"}
    annots = []
    seqs = []
    limits_x = []
    limits_y = []
    for i in U.index:
        annots.append(ax.arrow(0, 0,
                               U.loc[i, axis_1] * .6,
                               U.loc[i, axis_2] * .6,
                               color=acmap[i],
                               alpha=0.8,
                               lw=0.75,
                               ec = "black",
                               length_includes_head=True,
                               head_width=.03, width=.009))
        limits_x.append(U.loc[i, axis_1] * .8)
        limits_y.append(U.loc[i, axis_2] * .8)
        ax.text(U.loc[i, axis_1] * .6,
                U.loc[i, axis_2] * .6,
                str(i), zorder=-1)
        seqs.append(i)
    
    # set axis limits
    ax.set_xlim(min(limits_x), max(limits_x))
    ax.set_ylim(min(limits_y), max(limits_y))

    # Hide grid lines
    ax.grid(False)
    ax.set_facecolor("#f0f0f0")

    # get axis labels
    ax.set_xlabel("%s (%.2f%%)" % (axis_1, p.loc[axis_1] * 100),
                 fontsize=16, color="#000000")
    ax.set_ylabel("%s (%.2f%%)" % (axis_2, p.loc[axis_2] * 100),
                 fontsize=16, color="#000000")
    plt.show()



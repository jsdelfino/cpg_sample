# cpg_sample

A sample program to experiment with [Joern](https://github.com/joernio/joern)
and [Atom](https://github.com/AppThreat/atom).

/app/requests contains a copy of an old version of the
[Request](https://github.com/psf/requests) source code.

Joern and Atom are used to analyze that source code and generate graphml
representations of Code Property Graphs (CPGs) for it.

Install podman:
```
sudo dnf install podman
```

Use Joern to generate a CPG bin and a graphml export under
/graph/joern/export:

```
./joern.sh
```

Use Atom to generate an Atom file and graphml exports under
/graph/atom/export:

```
./atom.sh
```

Install the Python dependencies:
```
python -m venv .venv
. .venv/bin/activate
pip install networkx
```

Load the Joern export, print a sample method call graph, shortest path
between two methods, and the callers of a method:

```
python ./sample.py 2>&1 | tee joern_sample.log
```

Do the same with the Atom exports:

```
USE_ATOM=true python ./sample.py 2>&1 | tee atom_sample.log
```

The Atom version doesn't work yet. The following issues have been opened in
the Atom project:

https://github.com/AppThreat/atom/issues/187

https://github.com/AppThreat/atom/issues/188


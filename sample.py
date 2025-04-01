import glob
import os

import networkx as nx


# Check whether we want to use Atom instead of Joern
USE_ATOM = os.environ.get("USE_ATOM", "false") == "true"


if USE_ATOM:
    # Load the generated graphs into a single graph
    graph = nx.DiGraph()
    files = glob.glob("graph/atom/export/*.graphml")
    for file in files:
        print(file)
        g = nx.read_graphml(file)
        for node in g.nodes:
            g.nodes[node]["source_file"] = file
        graph.update(g)
else:
    # Load the generated graph
    graph = nx.read_graphml("graph/joern/export/export.xml")


# Build an index of methods
methods = {}
for node, attrs in graph.nodes(data=True):
    if attrs.get("labelV") == "METHOD":
        method_name = attrs.get("FULL_NAME").strip()
        methods[method_name] = node

print(
    f"Graph has {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges."
)


# Print a sorted list of method names
print("Loaded methods:")
for method in sorted(list(methods.keys())):
    print(method)


if USE_ATOM:
    # Connect call nodes to their target methods
    for node, attrs in graph.nodes(data=True):
        if attrs.get("labelV") == "CALL":
            method_name = attrs.get("METHOD_FULL_NAME").strip()
            target = methods.get(method_name)
            if target is not None:
                graph.add_edge(node, target)


# Print the call graph of a method
def print_call_graph(graph, node, m_depth, g_depth, visited):
    if node in visited:
        return
    visited[node] = True

    # Print method name
    attrs = graph.nodes[node]
    label = attrs.get("labelV")
    if label == "METHOD":
        name = attrs.get("FULL_NAME").strip()
        if name is not None:
            print("  " * m_depth + f"Method {name}")
            m_depth += 1

    # Limit recursion
    if g_depth > 100:
        return

    # Continue with successors
    for successor in graph.successors(node):
        print_call_graph(graph, successor, m_depth, g_depth + 1, visited)


# Convert a list of nodes to a list of method names
def method_names(graph, nodes):
    names = []
    for node in nodes:
        attrs = graph.nodes[node]
        label = attrs.get("labelV")
        if label == "METHOD":
            name = attrs.get("FULL_NAME").strip()
            if name is not None:
                names.append(name)
    return names


# Return all the call paths from a source method to a target method
def call_paths(graph, source, target):
    path = nx.shortest_path(graph, source=source, target=target)
    paths = [method_names(graph, path)]
    return paths


# Return all the direct and indirect callers of a method
def callers(graph, target):
    reversed_graph = graph.reverse()
    reachable_nodes = nx.descendants(reversed_graph, target)
    return method_names(graph, reachable_nodes)


# Print a call graph for method prepare_body
prepare_body = (
    "requests/src/requests/models.py:<module>.PreparedRequest.prepare_body"
)
print(f"Call graph for {prepare_body}:")
visited = {}
print_call_graph(graph, methods[prepare_body], 0, 0, visited)


# Print the call paths between test_urlencoded and prepare_body
test_urlencoded = "requests/tests/test_requests.py:<module>.TestRequests.test_urlencoded_get_query_multivalued_param"
paths = call_paths(graph, methods[test_urlencoded], methods[prepare_body])
for path in paths:
    print("Path:")
    for method_name in path:
        print(f"Segment {method_name}")


# Print the direct and indirect callers of prepare_body
print("Callers:")
for caller in callers(graph, methods[prepare_body]):
    print(f"Caller {caller}")

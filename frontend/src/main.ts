import "./style.css";
import Graph from "graphology";
import Sigma from "sigma";

const graph = new Graph();

const nodesReq = fetch("/data/nodes.json").then((r) => r.json());
const edgesReq = fetch("/data/edges.json").then((r) => r.json());
const channelsReq = fetch("/data/filtered_channels.json").then((r) => r.json());

Promise.all([nodesReq, edgesReq, channelsReq]).then(
  ([nodes, edges, channels]) => {
    console.log(nodes);
    for (const node in nodes) {
      const name = channels.find((c: any) => c.id === node).name;
      graph.addNode(node, {
        label: name,
        x: nodes[node][0],
        y: nodes[node][1],
        size: 2,
      });
    }

    for (const edge of edges) {
      graph.addEdge(edge.split("-")[0], edge.split("-")[1], { size: 0.5 });
    }

    const sigmaInstance = new Sigma(graph, document.getElementById("app")!);
  },
);

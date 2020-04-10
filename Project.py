from tkinter import *
from collections import deque, namedtuple
from PIL import Image,ImageTk

window = Tk()
window.geometry("700x1080")
window.title("LPU NAVIGATOR")

inf = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')
nodes=["LPU Main Gate", "Uni Hospital", "CC", "Uni Mall", "Mittal School of Business",
       "Baldev Raj Mittal Auditorium", "Admission Block", "Block 29","Block 28","Block 27",
       "Block 26","Block 25","Block 36","Block 37","Block 38","Block 32","Block 33",
       "Block 34","Open Audi","BH1","BH2","BH3","BH4"]


def s1():
    x=sourceList.curselection()
    a=sourceList.get(x)
    t1.insert(END,a)

def d1():
    y=destinationList.curselection()
    b=destinationList.get(y)
    t2.insert(END,b)

def reset():
    t1.delete("1.0","end")
    t2.delete("1.0","end")
    text.delete("1.0","end")


def path():
    def make_edge(start, end, cost=1):
        return Edge(start, end, cost)

    a=t1.get(1.0,END)
    b=t2.get(1.0,END)
    a=a.strip()
    b=b.strip()
    print(a,b)

    class Graph:
        def __init__(self, edges):
            # let's check that the data is right
            wrong_edges = [i for i in edges if len(i) not in [2, 3]]
            if wrong_edges:
                raise ValueError('Wrong edges data: {}'.format(wrong_edges))

            self.edges = [make_edge(*edge) for edge in edges]

        @property
        def vertices(self):
            return set(
                sum(
                    ([edge.start, edge.end] for edge in self.edges), []
                )
            )

        def get_node_pairs(self, n1, n2, both_ends=True):
            if both_ends:
                node_pairs = [[n1, n2], [n2, n1]]
            else:
                node_pairs = [[n1, n2]]
            return node_pairs

        def remove_edge(self, n1, n2, both_ends=True):
            node_pairs = self.get_node_pairs(n1, n2, both_ends)
            edges = self.edges[:]
            for edge in edges:
                if [edge.start, edge.end] in node_pairs:
                    self.edges.remove(edge)

        def add_edge(self, n1, n2, cost=1, both_ends=True):
            node_pairs = self.get_node_pairs(n1, n2, both_ends)
            for edge in self.edges:
                if [edge.start, edge.end] in node_pairs:
                    return ValueError('Edge {} {} already exists'.format(n1, n2))

            self.edges.append(Edge(start=n1, end=n2, cost=cost))
            if both_ends:
                self.edges.append(Edge(start=n2, end=n1, cost=cost))

        @property
        def neighbours(self):
            neighbours = {vertex: set() for vertex in self.vertices}
            for edge in self.edges:
                neighbours[edge.start].add((edge.end, edge.cost))

            return neighbours

        def dijkstra(self, source, dest):
            assert source in self.vertices, 'Such source node doesn\'t exist'
            distances = {vertex: inf for vertex in self.vertices}
            previous_vertices = {
                vertex: None for vertex in self.vertices
            }
            distances[source] = 0
            vertices = self.vertices.copy()

            while vertices:
                current_vertex = min(
                     vertices, key=lambda vertex: distances[vertex])
                vertices.remove(current_vertex)
                if distances[current_vertex] == inf:
                    break
                for neighbour, cost in self.neighbours[current_vertex]:
                    alternative_route = distances[current_vertex] + cost
                    if alternative_route < distances[neighbour]:
                        distances[neighbour] = alternative_route
                        previous_vertices[neighbour] = current_vertex

            path, current_vertex = deque(), dest
            while previous_vertices[current_vertex] is not None:
                path.appendleft(current_vertex)
                current_vertex = previous_vertices[current_vertex]
            if path:
                path.appendleft(current_vertex)
            return path


    graph = Graph([
        ("LPU Main Gate", "Uni Hospital", 10),  ("Uni Hospital", "CC",3 ),  ("Uni Hospital", "Uni Mall", 5), ("Uni Mall", "Mittal School of Business", 3),
    ("Uni Mall", "Baldev Raj Mittal Auditorium", 1), ("Mittal School of Business", "Baldev Raj Mittal Auditorium", 3), ("Mittal School of Business", "Admission Block", 5),
        ("Baldev Raj Mittal Auditorium", "Admission Block", 6),("Admission Block", "Block 29", 1),("Block 29", "Block 28", 1),("Block 28", "Block 27", 1),("Block 27", "Block 26", 1),
        ("Block 26", "Block 25", 1),("Admission Block", "Block 32", 2),("Block 33", "Block 34", 1),("Block 32", "Block 33", 1),("Block 33", "Block 36", 2),("Open Audi", "Block 36", 1),
        ("Block 36", "Block 37", 1),("Block 37", "Block 38", 2),("Block 27", "Block 38", 2),("Block 25", "BH1", 10),("BH1", "BH2", 7),("BH2", "BH3", 3),
    ("BH3", "BH4", 3),("Uni Hospital", "LPU Main Gate", 10),  ("CC", "Uni Hospital", 3),("Uni Mall", "Uni Hospital", 5), ("Mittal School of Business", "Uni Mall", 3),
    ("Baldev Raj Mittal Auditorium", "Uni Mall", 1), ( "Baldev Raj Mittal Auditorium", "Mittal School of Business",  3), ("Admission Block","Mittal School of Business",  5),
        ("Admission Block", "Baldev Raj Mittal Auditorium",  6),( "Block 29","Admission Block" ,1),(  "Block 28", "Block 29",1),( "Block 27", "Block 28",1),( "Block 26", "Block 27",1),
        ("Block 25", "Block 26",1),( "Block 32", "Admission Block",2),("Block 34","Block 33", 1),( "Block 33","Block 32", 1),( "Block 36", "Block 33", 2),( "Block 36", "Open Audi", 1),
        ("Block 37","Block 37",  1),( "Block 38","Block 37",  2),( "Block 38","Block 27",  2),( "BH1","Block 25",  10),( "BH2","BH1", 7),( "BH3","BH2", 3),
    ("BH4","BH3", 3)
    ])

    de = graph.dijkstra(a, b)
    a = graph.edges
    b = []
    c = []
    for j in range(len(de)-1):
        for i in a:
            if i.start == de[j] and i.end == de[j+1]:
                b.append(i.cost)

    for i in range(len(de)-1):
        c.append("Walk " + str(b[i]) + " units to " + de[i+1] + " from " + de[i])
    c.append("You have arrived to your destination, total distance covered is: %d units" % sum(b))
    text.insert(END,".\n".join(c))


sr=Label(window,text="Source :",background="lightgrey", relief=RAISED,pady=3)
sr.config(font=("Times",24,'bold'))
sourceList = Listbox(window,selectmode=SINGLE)
sourceList.insert(0,"LPU Main Gate")
sourceList.insert(1,"Uni Hospital")
sourceList.insert(2,"CC")
sourceList.insert(3,"Uni Mall")
sourceList.insert(4,"Mittal School of Business")
sourceList.insert(5,"Baldev Raj Mittal Auditorium")
sourceList.insert(6,"Admission Block")
sourceList.insert(7,"Block 29")
sourceList.insert(8,"Block 28")
sourceList.insert(9,"Block 27")
sourceList.insert(10,"Block 26")
sourceList.insert(11,"Block 25")
sourceList.insert(12,"Block 36")
sourceList.insert(13,"Block 37")
sourceList.insert(14,"Block 38")
sourceList.insert(15,"Block 32")
sourceList.insert(16,"Block 33")
sourceList.insert(17,"Block 34")
sourceList.insert(18,"Open Audi")
sourceList.insert(19,"BH1")
sourceList.insert(20,"BH2")
sourceList.insert(21,"BH3")
sourceList.insert(22,"BH4")

des=Label(window,text="Destination :",background="lightgrey", relief=RAISED,pady=3)
des.config(font=("Times",24,'bold'))
destinationList = Listbox(window,selectmode=SINGLE)
destinationList.insert(0,"LPU Main Gate")
destinationList.insert(1,"Uni Hospital")
destinationList.insert(2,"CC")
destinationList.insert(3,"Uni Mall")
destinationList.insert(4,"Mittal School of Business")
destinationList.insert(5,"Baldev Raj Mittal Auditorium")
destinationList.insert(6,"Admission Block")
destinationList.insert(7,"Block 29")
destinationList.insert(8,"Block 28")
destinationList.insert(9,"Block 27")
destinationList.insert(10,"Block 26")
destinationList.insert(11,"Block 25")
destinationList.insert(12,"Block 36")
destinationList.insert(13,"Block 37")
destinationList.insert(14,"Block 38")
destinationList.insert(15,"Block 32")
destinationList.insert(16,"Block 33")
destinationList.insert(17,"Block 34")
destinationList.insert(18,"Open Audi")
destinationList.insert(19,"BH1")
destinationList.insert(20,"BH2")
destinationList.insert(21,"BH3")
destinationList.insert(22,"BH4")

image = Image.open("LPU diagram.png")
LPU_map = ImageTk.PhotoImage(image)
label = Label(image = LPU_map)


x=IntVar()
y=IntVar()

b1=Button(window,text="Select",command=s1,background="lightgrey",borderwidth=3,pady=3)
b2=Button(window,text="Select",command=d1,background="lightgrey",borderwidth=3,pady=3)

b3=Button(window,text="Find Path",command=path,background="lightgrey",borderwidth=3,pady=3)
b3.config(font=("Times",16,'bold'))

b4=Button(window,text="Reset",command=reset,background="lightgrey",borderwidth=3,pady=3)
b4.config(font=("Times",16,'bold'))

t1=Text(window,height=2,width=20,pady=3)
t2=Text(window,height=2,width=20,pady=3)
text=Text(window,height=4,width=70,pady=3)



sr.grid(row=0,column=1)
sourceList.grid(row=1,column=1)
des.grid(row=0,column=2)
destinationList.grid(row=1,column=2)
b1.grid(row=2,column=1)
b2.grid(row=2,column=2)

t1.grid(row=3,column=1)
t2.grid(row=3,column=2)

b3.grid(row=4,column=1)
b4.grid(row=4,column=2)
text.grid(row=5,column=1,columnspan=2)
label.grid(row=6,column=1,columnspan=2)

window.mainloop()

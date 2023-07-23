from tkinter import *
from math import dist
from itertools import combinations


def get_line(x1, y1, x2, y2, r1, r2):
    y = -2*y1+2*y2
    x = -2*x1+2*x2
    i = x1*x1+y1*y1-x2*x2-y2*y2
    r = r1*r1-r2*r2
    return -x/y, (-i+r)/y


def get_intersect(x1, i1, x2, i2):
    x = x1-x2
    i = i2-i1
    x = i/x
    y = x1*x+i1
    return x, y


class Triangulation:
    def __init__(self):
        self.win = Tk()
        self.win.geometry("700x800")

        self.canvas = Canvas(self.win, width=700, height=550)
        self.canvas.grid(row=0, column=0, columnspan=4)

        self.lx = IntVar()
        self.ly = IntVar()

        self.lx.set(150)
        self.ly.set(150)

        self.points = [
            (IntVar(), IntVar()),
            (IntVar(), IntVar()),
            (IntVar(), IntVar()),
        ]
        self.points[0][0].set(300)
        self.points[0][1].set(100)
        self.points[1][0].set(200)
        self.points[1][1].set(200)
        self.points[2][0].set(300)
        self.points[2][1].set(300)

        self.distances = []
        self.update_distances()

    def update_distances(self):
        self.distances = [
            dist((self.lx.get(), self.ly.get()), (self.points[0][0].get(), self.points[0][1].get())),
            dist((self.lx.get(), self.ly.get()), (self.points[1][0].get(), self.points[1][1].get())),
            dist((self.lx.get(), self.ly.get()), (self.points[2][0].get(), self.points[2][1].get())),
        ]

    def setup(self):
        loop = [
            ("Location X Value", self.lx, "Location Y Value", self.ly),
            ("Point 1 X Value", self.points[0][0], "Point 1 Y Value", self.points[0][1]),
            ("Point 2 X Value", self.points[1][0], "Point 2 Y Value", self.points[1][1]),
            ("Point 3 X Value", self.points[2][0], "Point 3 Y Value", self.points[2][1]),
        ]

        for i, t in enumerate(loop):
            text1, var1, text2, var2 = t
            l = Label(self.win, text=text1)
            l.grid(row=i+1, column=0, sticky="e")
            s = Scale(self.win, variable=var1, from_=0, to=700, orient=HORIZONTAL, command=self.update)
            s.grid(row=i+1, column=1, sticky="w")
            l = Label(self.win, text=text2)
            l.grid(row=i+1, column=2, sticky="e")
            s = Scale(self.win, variable=var2, from_=0, to=700, orient=HORIZONTAL, command=self.update)
            s.grid(row=i+1, column=3, sticky="w")

        '''
        l = Label(self.win, text="Red = Triangulation Points")
        l.grid(row=2, column=0, columnspan=4)
        l = Label(self.win, text="Green = Location")
        l.grid(row=3, column=0, columnspan=4)
        l = Label(self.win, text="Yellow = Prediction")
        l.grid(row=4, column=0, columnspan=4)
        '''

    def run(self):
        self.update()
        self.setup()

        self.win.mainloop()

    def predict(self):
        # x1, intercept1
        x1, i1 = get_line(self.points[0][0].get(), self.points[0][1].get(),
                          self.points[1][0].get(), self.points[1][1].get(),
                          self.distances[0], self.distances[1])
        x2, i2 = get_line(self.points[1][0].get(), self.points[1][1].get(),
                          self.points[2][0].get(), self.points[2][1].get(),
                          self.distances[1], self.distances[2])
        return get_intersect(x1, i1, x2, i2)


    def update(self, event=None):
        self.canvas.delete('all')

        self.update_distances()

        # self.canvas.create_rectangle(self.lx.get() - 2, self.ly.get() - 2, self.lx.get() + 2, self.ly.get() + 2,
        #                              fill="green", outline="green")

        for t, d in zip(self.points, self.distances):
            x, y = t
            x = x.get()
            y = y.get()
            self.canvas.create_rectangle(x - 2, y - 2, x + 2, y + 2, fill="red", outline="red")
            self.canvas.create_oval(x - d, y - d, x + d, y + d)

        px, py = self.predict()
        print(px, py)
        self.canvas.create_rectangle(px - 2, py - 2, px + 2, py + 2, fill="orange", outline="orange")


def main():
    triangulation = Triangulation()
    triangulation.run()


if __name__ == '__main__':
    main()

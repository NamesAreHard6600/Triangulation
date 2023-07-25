from tkinter import *
from math import dist
from line import Line


class Trilateration:
    def __init__(self):
        self.error_text, self.error = None, None

        self.win = Tk()
        self.win.geometry("700x800")

        self.canvas = Canvas(self.win, width=700, height=550)
        self.canvas.grid(row=0, column=0, columnspan=4)

        self.lx = IntVar()
        self.ly = IntVar()

        self.lx.set(309)
        self.ly.set(247)

        self.points = [
            (IntVar(), IntVar()),
            (IntVar(), IntVar()),
            (IntVar(), IntVar()),
        ]

        self.points[0][0].set(288)
        self.points[0][1].set(100)
        self.points[1][0].set(175)
        self.points[1][1].set(350)
        self.points[2][0].set(484)
        self.points[2][1].set(329)

        self.distances = []
        self.update_distances()

        self.setup()
        self.update()

    def update_distances(self):
        self.distances = [
            dist((self.lx.get(), self.ly.get()), (self.points[0][0].get(), self.points[0][1].get())),
            dist((self.lx.get(), self.ly.get()), (self.points[1][0].get(), self.points[1][1].get())),
            dist((self.lx.get(), self.ly.get()), (self.points[2][0].get(), self.points[2][1].get())),
        ]

    def get_line(self, x1, y1, x2, y2, r1, r2):
        y = -2 * y1 + 2 * y2
        x = -2 * x1 + 2 * x2
        i = x1 * x1 + y1 * y1 - x2 * x2 - y2 * y2
        r = r1 * r1 - r2 * r2
        # Division by Zero Error: y cords are the same: Compare
        # All three the same; two solutions
        # Basically, a vertical line, but that's hard to represent
        if y != 0:
            return Line(-x / y, (-i + r) / y)
        if x != 0:
            return Line(0, (-i + r) / x, True)
        self.error_text.set("ERROR: Two Points are on the Exact Same Coordinate")
        return

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

        self.error_text = StringVar()
        self.error = Label(self.win, textvariable=self.error_text, fg="red", font=("Arial", 18))
        self.error.grid(row=5, column=0, columnspan=4)


    def run(self):
        self.win.mainloop()

    def predict(self):
        # x1, intercept1
        l1 = self.get_line(self.points[0][0].get(), self.points[0][1].get(),
                           self.points[1][0].get(), self.points[1][1].get(),
                           self.distances[0], self.distances[1])
        l2 = self.get_line(self.points[1][0].get(), self.points[1][1].get(),
                           self.points[2][0].get(), self.points[2][1].get(),
                           self.distances[1], self.distances[2])
        # We only technically need 2 lines, but 3 lines provide some protection
        l3 = self.get_line(self.points[0][0].get(), self.points[0][1].get(),
                           self.points[2][0].get(), self.points[2][1].get(),
                           self.distances[0], self.distances[2])
        # Uncomment for visual indication of what is happening
        self.visualize(l1, l2, l3)

        if self.error_text.get() != "":
            return

        return l1.get_intersect(l2, l3, self)

    def visualize(self, *args):
        for l in args:
            if l:
                l.draw(self.canvas)

    def update(self, event=None):
        self.canvas.delete('all')
        self.error_text.set("")

        self.update_distances()

        for t, d in zip(self.points, self.distances):
            x, y = t
            x = x.get()
            y = y.get()
            self.canvas.create_rectangle(x - 2, y - 2, x + 2, y + 2, fill="red", outline="red")
            self.canvas.create_oval(x - d, y - d, x + d, y + d)

        try:
            px, py = self.predict()
        except TypeError:  # There was an error in predicting so None was returned
            pass
        else:
            self.canvas.create_rectangle(px - 4, py - 4, px + 4, py + 4, fill="orange", outline="orange")

        self.canvas.create_rectangle(self.lx.get() - 2, self.ly.get() - 2, self.lx.get() + 2, self.ly.get() + 2,
                                     fill="green", outline="green")
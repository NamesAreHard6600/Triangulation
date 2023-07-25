from tkinter import *
from math import dist
from line import Line


# x^2 - 2xx1 + x1^2 + y^2 - 2yy1 + y1^2 = r1^2
# Takes two circles and finds the line where they intersect
def get_line(x1, y1, x2, y2, r1, r2):
    y = -2*y1+2*y2
    x = -2*x1+2*x2
    i = x1*x1+y1*y1-x2*x2-y2*y2
    r = r1*r1-r2*r2
    # Division by Zero Error: y cords are the same: Compare
    # All three the same; two solutions
    return -x/y, (-i+r)/y


# Takes two lines and finds where they intersect
# After getting two lines from get_line, this finds where they intersect and therefore where the circles intersect
def get_intersect(x1, i1, x2, i2):
    x = x1-x2
    i = i2-i1
    try:
        x = i/x
    except ZeroDivisionError:
        pass  # Just Ignore
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

        self.distances = [DoubleVar(), DoubleVar(), DoubleVar()]
        self.update_distances()

    def update_distances(self):
        self.distances[0].set(dist((self.lx.get(), self.ly.get()), (self.points[0][0].get(), self.points[0][1].get())))
        self.distances[1].set(dist((self.lx.get(), self.ly.get()), (self.points[1][0].get(), self.points[1][1].get())))
        self.distances[2].set(dist((self.lx.get(), self.ly.get()), (self.points[2][0].get(), self.points[2][1].get())))

    def setup(self):
        row = 1
        loop = [
            # ("Location X Value", self.lx, "Location Y Value", self.ly),
            ("Point 1 X Value", self.points[0][0], "Point 1 Y Value", self.points[0][1]),
            ("Point 2 X Value", self.points[1][0], "Point 2 Y Value", self.points[1][1]),
            ("Point 3 X Value", self.points[2][0], "Point 3 Y Value", self.points[2][1]),
        ]

        for t in loop:
            text1, var1, text2, var2 = t
            l = Label(self.win, text=text1)
            l.grid(row=row, column=0, sticky="e")
            s = Scale(self.win, variable=var1, from_=0, to=700, orient=HORIZONTAL, command=self.update)
            s.grid(row=row, column=1, sticky="w")
            l = Label(self.win, text=text2)
            l.grid(row=row, column=2, sticky="e")
            s = Scale(self.win, variable=var2, from_=0, to=700, orient=HORIZONTAL, command=self.update)
            s.grid(row=row, column=3, sticky="w")
            row += 1

        loop = [
            ("Point 1 Distance", self.distances[0]),
            ("Point 2 Distance", self.distances[1]),
            ("Point 3 Distance", self.distances[2]),
        ]

        for i, t in enumerate(loop):
            text, var = t
            l = Label(self.win, text=text)
            l.grid(row=row, column=0, columnspan=2, sticky="e")
            s = Scale(self.win, variable=var, from_=0, to=1000, orient=HORIZONTAL, command=self.update)
            s.grid(row=row, column=2, columnspan=2, sticky="w")
            row += 1


    def run(self):
        self.update()
        self.setup()

        self.win.mainloop()

    def predict(self):
        if self.points[0][1].get() == self.points[1][1].get() == self.points[2][1].get():
            raise(Exception("All three points are the same y value"))
        # To prevent divide by zero errors, a lot has to happen
        if self.points[0][1].get() == self.points[1][1].get():
            x1, i1 = get_line(self.points[0][0].get(), self.points[0][1].get(),
                              self.points[2][0].get(), self.points[2][1].get(),
                              self.distances[0].get(), self.distances[2].get())
            x2, i2 = get_line(self.points[1][0].get(), self.points[1][1].get(),
                              self.points[2][0].get(), self.points[2][1].get(),
                              self.distances[1].get(), self.distances[2].get())
        elif self.points[1][1].get() == self.points[2][1].get():
            x1, i1 = get_line(self.points[0][0].get(), self.points[0][1].get(),
                              self.points[1][0].get(), self.points[1][1].get(),
                              self.distances[0].get(), self.distances[1].get())
            x2, i2 = get_line(self.points[0][0].get(), self.points[0][1].get(),
                              self.points[2][0].get(), self.points[2][1].get(),
                              self.distances[0].get(), self.distances[2].get())
        else:
            x1, i1 = get_line(self.points[0][0].get(), self.points[0][1].get(),
                              self.points[1][0].get(), self.points[1][1].get(),
                              self.distances[0].get(), self.distances[1].get())
            x2, i2 = get_line(self.points[1][0].get(), self.points[1][1].get(),
                              self.points[2][0].get(), self.points[2][1].get(),
                              self.distances[1].get(), self.distances[2].get())
        # Uncomment for visual indication of what is happening
        self.draw_line(x1, i1)
        self.draw_line(x2, i2)
        return get_intersect(x1, i1, x2, i2)


    def update(self, event=None):
        self.canvas.delete('all')

        # self.update_distances()

        for t, d in zip(self.points, self.distances):
            x, y = t
            x, y, d = x.get(), y.get(), d.get()
            self.canvas.create_rectangle(x - 2, y - 2, x + 2, y + 2, fill="red", outline="red")
            self.canvas.create_oval(x - d, y - d, x + d, y + d)

        px, py = self.predict()
        self.canvas.create_rectangle(px - 4, py - 4, px + 4, py + 4, fill="orange", outline="orange")

        # self.canvas.create_rectangle(self.lx.get() - 2, self.ly.get() - 2, self.lx.get() + 2, self.ly.get() + 2,
        #                              fill="green", outline="green")


    def draw_line(self, x, i):
        self.canvas.create_line(0, i, 1000, x*1000+i, fill="green")


def main():

    triangulation = Triangulation()
    triangulation.run()


if __name__ == '__main__':
    main()

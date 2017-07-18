"""
Created on 24. 4. 2015

@author: janbednarik
"""

from ptcpy.trajectory_clustering.common import euclid_dist


class Trajectory(object):
    """A class implementing one trajectory"""

    def __init__(self, id, distance=euclid_dist):
        self.id = id
        self.points = []
        self.ci = -1
        self.distance = distance
        self.prefix_sum = [0.0]

    def add_point(self, p):
        # compute prefix sum
        if len(self.points) > 0:
            self.prefix_sum.append(self.prefix_sum[len(self.prefix_sum) - 1] +
                                   self.distance(p, self.points[len(self.points) - 1]))

        # add point
        self.points.append(p)

    def get_id(self):
        return self.id

    def get_points(self):
        return self.points

    def get_prefix_sum(self):
        return self.prefix_sum

    def get_cluster_idx(self):
        return self.ci

    def set_cluster_idx(self, ci):
        self.ci = ci

    def length(self):
        return self.prefix_sum[len(self.prefix_sum) - 1]

    def draw(self, widget, color, x_offset=0, y_offset=0):
        xlast, ylast = None, None
        for p in self.points:
            # paint a point
            x = p[0] + x_offset
            y = p[1] + y_offset
            widget.create_oval(x - 2, y - 2, x + 2, y + 2, fill=color)

            # paint a line
            if xlast is not None and ylast is not None:
                widget.create_line(xlast, ylast, x, y, smooth=True)
            xlast = x
            ylast = y

    def __str__(self):
        out = "=== Trajectory ===\n"
        out += "cluster: %d\n" % self.ci
        for p in self.points:
            out += repr(p) + ", "
        out += "\n"
        return out

    def __len__(self):
        return len(self.points)

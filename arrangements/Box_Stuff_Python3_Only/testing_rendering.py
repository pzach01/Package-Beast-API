from . import test_imports
from .test_imports import *
def draw_bin(ax,bin_width, bin_height, bin_depth, bin_edge_color='black'):
    ax.plot3D([0,bin_width], [0,0], [0, 0], bin_edge_color)
    ax.plot3D([0, 0], [0,bin_height], [0, 0], bin_edge_color)
    ax.plot3D([0,0], [0,0], [0, bin_depth], bin_edge_color)

    ax.plot3D([0,bin_width], [bin_height,bin_height], [0, 0], bin_edge_color)
    ax.plot3D([0,bin_width], [0,0], [bin_depth, bin_depth], bin_edge_color)
    ax.plot3D([0,bin_width], [bin_height,bin_height], [bin_depth, bin_depth], bin_edge_color)

    ax.plot3D([bin_width, bin_width], [0,bin_height], [0, 0], bin_edge_color)
    ax.plot3D([0, 0], [0,bin_height], [bin_depth, bin_depth], bin_edge_color)
    ax.plot3D([bin_width, bin_width], [0,bin_height], [bin_depth, bin_depth], bin_edge_color)

    ax.plot3D([bin_width,bin_width], [0,0], [0, bin_depth], bin_edge_color)
    ax.plot3D([0,0], [bin_height,bin_height], [0, bin_depth], bin_edge_color)
    ax.plot3D([bin_width,bin_width], [bin_height,bin_height], [0, bin_depth], bin_edge_color)

    ax.set_xlim(0,max(bin_width, bin_height, bin_depth))
    ax.set_ylim(0,max(bin_width, bin_height, bin_depth))
    ax.set_zlim(0,max(bin_width, bin_height, bin_depth))

def draw_boxes(ax,x_vals, y_vals, z_vals, widths, heights, depths):

    colors = ['red', 'green', 'blue', 'yellow', 'purple']
    for i in range(len(x_vals)):
        ax.scatter(x_vals[i], y_vals[i], z_vals[i], c=colors[i%len(colors)], marker='o')
        ax.scatter(x_vals[i]+widths[i], y_vals[i], z_vals[i], c=colors[i%len(colors)], marker='o')
        ax.scatter(x_vals[i], y_vals[i]+heights[i], z_vals[i], c=colors[i%len(colors)], marker='o')
        ax.scatter(x_vals[i]+widths[i], y_vals[i]+heights[i], z_vals[i], c=colors[i%len(colors)], marker='o')

        ax.scatter(x_vals[i], y_vals[i], z_vals[i]+depths[i], c=colors[i%len(colors)], marker='o')
        ax.scatter(x_vals[i]+widths[i], y_vals[i], z_vals[i]+depths[i], c=colors[i%len(colors)], marker='o')
        ax.scatter(x_vals[i], y_vals[i]+heights[i], z_vals[i]+depths[i], c=colors[i%len(colors)], marker='o')
        ax.scatter(x_vals[i]+widths[i], y_vals[i]+heights[i], z_vals[i]+depths[i], c=colors[i%len(colors)], marker='o')

        ax.plot3D([x_vals[i],x_vals[i]+widths[i]], [y_vals[i],y_vals[i]], [z_vals[i], z_vals[i]], colors[i%len(colors)])
        ax.plot3D([x_vals[i], x_vals[i]], [y_vals[i],y_vals[i]+heights[i]], [z_vals[i], z_vals[i]], colors[i%len(colors)])
        ax.plot3D([x_vals[i],x_vals[i]], [y_vals[i],y_vals[i]], [z_vals[i], z_vals[i]+depths[i]], colors[i%len(colors)])

        ax.plot3D([x_vals[i],x_vals[i]+widths[i]], [y_vals[i]+heights[i],y_vals[i]+heights[i]], [z_vals[i], z_vals[i]], colors[i%len(colors)])
        ax.plot3D([x_vals[i],x_vals[i]+widths[i]], [y_vals[i],y_vals[i]], [z_vals[i]+depths[i], z_vals[i]+depths[i]], colors[i%len(colors)])
        ax.plot3D([x_vals[i],x_vals[i]+widths[i]], [y_vals[i]+heights[i],y_vals[i]+heights[i]], [z_vals[i]+depths[i], z_vals[i]+depths[i]], colors[i%len(colors)])

        ax.plot3D([x_vals[i]+widths[i], x_vals[i]+widths[i]], [y_vals[i],y_vals[i]+heights[i]], [z_vals[i], z_vals[i]], colors[i%len(colors)])
        ax.plot3D([x_vals[i], x_vals[i]], [y_vals[i],y_vals[i]+heights[i]], [z_vals[i]+depths[i], z_vals[i]+depths[i]], colors[i%len(colors)])
        ax.plot3D([x_vals[i]+widths[i], x_vals[i]+widths[i]], [y_vals[i],y_vals[i]+heights[i]], [z_vals[i]+depths[i], z_vals[i]+depths[i]], colors[i%len(colors)])

        ax.plot3D([x_vals[i]+widths[i],x_vals[i]+widths[i]], [y_vals[i],y_vals[i]], [z_vals[i], z_vals[i]+depths[i]], colors[i%len(colors)])
        ax.plot3D([x_vals[i],x_vals[i]], [y_vals[i]+heights[i],y_vals[i]+heights[i]], [z_vals[i], z_vals[i]+depths[i]], colors[i%len(colors)])
        ax.plot3D([x_vals[i]+widths[i],x_vals[i]+widths[i]], [y_vals[i]+heights[i],y_vals[i]+heights[i]], [z_vals[i], z_vals[i]+depths[i]], colors[i%len(colors)])

def render_test():

    bin_width = 1800
    bin_height = 1800
    bin_depth = 2400
    import math
    bin_weight_capacity = math.inf
    container=ContainerPY3DBP('very-very-large-box', bin_width, bin_height, bin_depth, bin_weight_capacity)

    items = [
        ItemPY3DBP('50g [powder 2]', 450, 793, 975, 2),
        ItemPY3DBP('50g [powder 2]', 450, 793, 975, 2),
        ItemPY3DBP('50g [powder 2]', 450, 793, 975, 2),




        ]













    packer=single_pack.single_pack(container, items)

    if packer.bins[0].unfitted_items:
        raise Exception("doesn't fit")
        # print("'doesn't fit'")
    if not packer.bins[0].unfitted_items:
        #print("fits, yo!")


        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        x_vals = []
        y_vals = []
        z_vals = []
        widths = []
        heights = []
        depths = []

        for b in packer.bins:
            #print(":::::::::::", b.string())

            #print("FITTED ITEMS:")
            for item in b.items:
                #print("====> ", item.string())
                x_vals.append(float(item.position[0]))
                y_vals.append(float(item.position[1]))
                z_vals.append(float(item.position[2]))

                # print("width:", float(item.width), "height:", float(item.height), "depth:", float(item.depth))
                # print("dim_0:", item.get_dimension()[0], "dim_1:", item.get_dimension()[1], "dim_2:", item.get_dimension()[2])
                widths.append(float(item.get_dimension()[0]))
                heights.append(float(item.get_dimension()[1]))
                depths.append(float(item.get_dimension()[2]))

                #print(item.rotation_type)

            #print("UNFITTED ITEMS:")
            for item in b.unfitted_items:
                pass
                #print("====> ", item.string())

            #print("***************************************************")
            #print("***************************************************")



        draw_bin(ax,bin_width, bin_height, bin_depth)
        draw_boxes(ax,x_vals, y_vals, z_vals, widths, heights, depths)
        ax.set_xlabel('Width (x)')
        ax.set_ylabel('Height (y)')
        ax.set_zlabel('Depth (z)')

        plt.show()
        

render_test()
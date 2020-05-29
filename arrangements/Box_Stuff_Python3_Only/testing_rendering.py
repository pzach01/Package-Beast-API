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


def render(packer,bin_width, bin_height, bin_depth):
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

    render(packer, bin_width,bin_height,bin_depth)
    

def render_bug():
    bin_width = 20
    bin_height = 20
    bin_depth = 20
    import math
    bin_weight_capacity = math.inf
    container=ContainerPY3DBP('very-very-large-box', bin_width, bin_height, bin_depth, bin_weight_capacity)






    item1=ItemPY3DBP('1',14,20,20,1)
    item2=ItemPY3DBP('2',6,17,14,1)
    item3=ItemPY3DBP('3',3,18,6,1)
    item4=ItemPY3DBP('4',2,19,5,1)
    item5=ItemPY3DBP('5',6,3,8,1)
    #item6=ItemPY3DBP('',2,2,9,1)
    item6=ItemPY3DBP('bugaboo',2,2,9,1)
    #item7=ItemPY3DBP('',4,2,4,1)
    item7=ItemPY3DBP('7',4,2,4,1)

    items=[item1,item2,item3,item4,item5,item6,item7]

    #item6=ItemPY3DBP('',2,2,9,1)
    #item7=ItemPY3DBP('',4,2,4,1)











    packer=single_pack.single_pack(container, items)
    if packer==None:
        raise Exception("couldnt fit stuff")
    for item in packer.items:
        lowW,upperW=item.position[0], item.position[0]+item.get_dimension()[0]
        lowH,upperH=item.position[1], item.position[1]+item.get_dimension()[1]
        lowD,upperD=item.position[2], item.position[2]+item.get_dimension()[2]
        print(item.string())
        print(str(lowW)+'; '+str(upperW))
        print(str(lowH)+'; '+str(upperH))
        print(str(lowD)+'; '+str(upperD))

        print('\n')
    if packer==None:
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
render_bug()
render_test()


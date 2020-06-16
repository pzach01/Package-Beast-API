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
    if len(packer.unfit_items)>0:
        raise Exception("doesn't fit")
        # print("'doesn't fit'")
    else:
        #print("fits, yo!")


        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        x_vals = []
        y_vals = []
        z_vals = []
        widths = []
        heights = []
        depths = []


        for item in packer.items:
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
        ItemPY3DBP(str(ele), 450, 793, 975, 2) for ele in range(0, 17)



        ]













    packer=single_pack.single_pack(container, items,1000,True, True)

    render(packer, bin_width,bin_height,bin_depth)


def render_test2():
    container=ContainerPY3DBP('Container',25,6,15)
    # 17,2,10
    items=[
        ItemPY3DBP('1',17,2,10),
        ItemPY3DBP('2',14,4,7),
        ItemPY3DBP('3',19,3,5),
        ItemPY3DBP('4',19,3,8)
    ]
    
    '''
    coordinates={}
    
    coordinates[(8, 4, 5)]=(17, 2, 10)
    coordinates[(11, 0, 8)]=(14, 4, 7)
    coordinates[(6, 3, 0)]=(19, 3, 5)
    coordinates[(6, 0, 0)]=(19, 3, 8)
    from . import testing_underfitting
    from .testing_underfitting import render_something_that_failed
    render_something_that_failed(container,items,coordinates)
    '''

    packer=single_pack.single_pack(container, items)
    render(packer, container.xDim, container.yDim, container.zDim)



def recursive_bug():
    '''
    Container: Container(1x12x4, max_weight:100) vol(48)
    1(1.000000x4.000000x3.000000, weight: 1) pos(0.000000, 0.000000, 0.000000) rt(0) vol(12)
    2(1.000000x1.000000x1.000000, weight: 1) pos(0.000000, 0.000000, 0.000000) rt(0) vol(1)
    4(1.000000x2.000000x1.000000, weight: 1) pos(0.000000, 0.000000, 0.000000) rt(0) vol(2)
    6(1.000000x2.000000x1.000000, weight: 1) pos(0.000000, 0.000000, 0.000000) rt(0) vol(2)
    7(1.000000x2.000000x1.000000, weight: 1) pos(0.000000, 0.000000, 0.000000) rt(0) vol(2)
    8(1.000000x4.000000x2.000000, weight: 1) pos(0.000000, 0.000000, 0.000000) rt(0) vol(8)
    '''
    container=ContainerPY3DBP('very-very-large-box', 1, 12, 4)


    items = [
        ItemPY3DBP('1', 1, 5, 3),
        ItemPY3DBP('2', 1, 1, 1),
        ItemPY3DBP('3',1,3,3),
        ItemPY3DBP('4', 1, 2, 1),
        ItemPY3DBP('5',1,2,3),
        ItemPY3DBP('6', 1, 2, 1),
        ItemPY3DBP('7', 1, 2, 1),
        ItemPY3DBP('8', 1, 4, 2),
        
    ]

    packer=single_pack.single_pack(container, items,True, True)
    render(packer,container.xDim, container.yDim,container.zDim)
    assert (not (packer==None))
    testing_single_pack.test_for_double_fit(packer, 10000)
recursive_bug()
#render_test()
render_test2()

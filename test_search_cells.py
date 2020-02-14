import main
import numpy

root = main.Full_field()
root.find_next_node(root.x0, root.y0)
root.check_nodes()
matrix = numpy.full((main.cells_number, main.cells_number),
                    main.individual_cell())

obstacle_positions = [(2, 2), (3, 2), (4, 2), (5, 2)]


import numpy
import pyopencl, pyopencl.array

def make_vertices_np(nr, max_val=1024):
    """
    Generates a set of vertices as nr-tuple of 2-tuple of integers
    """
    return numpy.random.randint(0, max_val, nr * 2).reshape((nr, 2)).astype(numpy.float32)

if __name__ == "__main__":
    import time
    N = 24
    L = 1024
    vertices = make_vertices_np(N, L)
    print vertices

    ctx = pyopencl.create_some_context()
    queue = pyopencl.CommandQueue(ctx, 
                properties=pyopencl.command_queue_properties.PROFILING_ENABLE)
    src = open("inside_polygon.cl").read()
    prg = pyopencl.Program(ctx, src).build()

    t0 = time.time()
    d_vertices = pyopencl.array.to_device(queue, vertices)
    d_result = pyopencl.array.empty(queue, (L,L), numpy.uint8)
    evt = prg.insidePolygon(queue, (L,L), (32,1), 
                            d_vertices.data, numpy.int32(N), numpy.uint8(1), d_result.data)
    res = d_result.get()
    print("execution time OpenCL: %.3fs Actual kernel execution time: %.6fs" % (time.time() - t0, 1e-9 * (evt.profile.end - evt.profile.start)))
    msk = res

    import pylab
    pylab.imshow(msk)
    last = vertices[-1]
    for v in vertices:
        pylab.annotate("", xy=v, xytext=last, xycoords="data",
                 arrowprops=dict(arrowstyle="-"))
        last = v
    pylab.show()

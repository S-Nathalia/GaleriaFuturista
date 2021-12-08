import numpy as np


class CarregarObj:
    buffer = []

    @staticmethod
    def busca_dados(valores, coordenadas, skip, data_type):
        for d in valores:
            if d == skip:
                continue
            if data_type == 'float':
                coordenadas.append(float(d))
            elif data_type == 'int':
                coordenadas.append(int(d)-1)


    @staticmethod # sorted vertex buffer for use with glDrawArrays function
    def criar_vertex_buffer(indices_data, vertices, texturas, normals):
        for i, ind in enumerate(indices_data):
            if i % 3 == 0: # sort the vertex coordenadas
                inicio = ind * 3
                fim = inicio + 3
                CarregarObj.buffer.extend(vertices[inicio:fim])
            elif i % 3 == 1: # sort the texture coordenadas
                inicio = ind * 2
                fim = inicio + 2
                CarregarObj.buffer.extend(texturas[inicio:fim])
            elif i % 3 == 2: # sort the normal vectors
                inicio = ind * 3
                fim = inicio + 3
                CarregarObj.buffer.extend(normals[inicio:fim])


    @staticmethod # TODO unsorted vertex buffer for use with glDrawElements function
    def create_unsorted_vertex_buffer(indices_data, vertices, texturas, normals):
        num_verts = len(vertices) // 3

        for i1 in range(num_verts):
            inicio = i1 * 3
            fim = inicio + 3
            CarregarObj.buffer.extend(vertices[inicio:fim])

            for i2, data in enumerate(indices_data):
                if i2 % 3 == 0 and data == i1:
                    inicio = indices_data[i2 + 1] * 2
                    fim = inicio + 2
                    CarregarObj.buffer.extend(texturas[inicio:fim])

                    inicio = indices_data[i2 + 2] * 3
                    fim = inicio + 3
                    CarregarObj.buffer.extend(normals[inicio:fim])

                    break


    @staticmethod
    def exibir_buffer_data(buffer):
        for i in range(len(buffer)//8):
            inicio = i * 8
            fim = inicio + 8
            print(buffer[inicio:fim])


    @staticmethod
    def carregar_model(file, sorted=True):
        vert_coords = [] # will contain all the vertex coordenadas
        tex_coords = [] # will contain all the texture coordenadas
        norm_coords = [] # will contain all the vertex normals

        todos_indices = [] # will contain all the vertex, texture and normal indices
        indices = [] # will contain the indices for indexed drawing


        with open(file, 'r') as f:
            line = f.readline()
            while line:
                values = line.split()
                if len(values) != 0 :
                    if values[0] == 'v':
                        CarregarObj.busca_dados(values, vert_coords, 'v', 'float')
                    elif values[0] == 'vt':
                        CarregarObj.busca_dados(values, tex_coords, 'vt', 'float')
                    elif values[0] == 'vn':
                        CarregarObj.busca_dados(values, norm_coords, 'vn', 'float')
                    elif values[0] == 'f':
                        for value in values[1:]:
                            val = value.split('/')
                            CarregarObj.busca_dados(val, todos_indices, 'f', 'int')
                            indices.append(int(val[0])-1)

                line = f.readline()

        if sorted:
            # use with glDrawArrays
            CarregarObj.criar_vertex_buffer(todos_indices, vert_coords, tex_coords, norm_coords)
        else:
            # use with glDrawElements
            CarregarObj.create_unsorted_vertex_buffer(todos_indices, vert_coords, tex_coords, norm_coords)

        # CarregarObj.exibir_buffer_data(CarregarObj.buffer)

        buffer = CarregarObj.buffer.copy() # create a local copy of the buffer list, otherwise it will overwrite the static field buffer
        CarregarObj.buffer = [] # after copy, make sure to set it back to an empty list

        return np.array(indices, dtype='uint32'), np.array(buffer, dtype='float32')

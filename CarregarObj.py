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


    @staticmethod # buffer de vértice classificado para uso com função glDrawArrays
    def criar_vertex_buffer(indices_data, vertices, texturas, normals):
        for i, ind in enumerate(indices_data):
            if i % 3 == 0: # ordena o vertex coordenadas
                inicio = ind * 3
                fim = inicio + 3
                CarregarObj.buffer.extend(vertices[inicio:fim])
            elif i % 3 == 1: # ordena o texture coordenadas
                inicio = ind * 2
                fim = inicio + 2
                CarregarObj.buffer.extend(texturas[inicio:fim])
            elif i % 3 == 2: # ordena o normal vectors
                inicio = ind * 3
                fim = inicio + 3
                CarregarObj.buffer.extend(normals[inicio:fim])


    @staticmethod
    def criar_nordenado_vertex_buffer(indices_data, vertices, texturas, normals):
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
        vert_coords = [] # ira conter todos os vertices de coordenadas
        tex_coords = [] # todas as coordenadas de texturas
        norm_coords = [] # todos vertex normals

        todos_indices = [] # ira conter os normal vertices, texturas
        indices = [] # ira conter os indices de desenhar


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
            # glDrawArrays
            CarregarObj.criar_vertex_buffer(todos_indices, vert_coords, tex_coords, norm_coords)
        else:
            # glDrawElements
            CarregarObj.criar_nordenado_vertex_buffer(todos_indices, vert_coords, tex_coords, norm_coords)

        buffer = CarregarObj.buffer.copy() # criar uma copia para nao sobreescrever o campo estatico
        CarregarObj.buffer = [] # para mexer na lista vazia novamente depois de copiar

        return np.array(indices, dtype='uint32'), np.array(buffer, dtype='float32')

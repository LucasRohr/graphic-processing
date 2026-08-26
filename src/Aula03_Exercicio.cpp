#include <iostream>
#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>
#include <vector>
#include <cmath>

GLFWwindow* Window = nullptr;
GLuint Shader_programm = 0;
GLuint Vao = 0;
int WIDTH = 800;
int HEIGHT = 800;

void redimensionaCallback(GLFWwindow* window, int w, int h) {
    WIDTH = w;
    HEIGHT = h;
}

void inicializaOpenGL() {
    // Inicializa GLFW
    if (!glfwInit()) {
        std::cerr << "Falha ao inicializar o GLFW" << std::endl;
        exit(EXIT_FAILURE);
    }

    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE); // Obrigatório no macOS

    // Criação de uma janela
    Window = glfwCreateWindow(WIDTH, HEIGHT, "Exemplo - renderizacao de um triangulo", NULL, NULL);
    
    // Caso não seja possível criar a janela, a GLFW e a aplicação são terminadas
    if (!Window) {
        glfwTerminate();
        exit(EXIT_FAILURE);
    }

    glfwSetWindowSizeCallback(Window, redimensionaCallback);
    glfwMakeContextCurrent(Window);

    // inicializar o GLAD
    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress)) {
        std::cerr << "Falha ao inicializar o GLAD" << std::endl;
        exit(EXIT_FAILURE);
    }

    std::cout << "Placa de video: " << glGetString(GL_RENDERER) << std::endl;
    std::cout << "Versao do OpenGL: " << glGetString(GL_VERSION) << std::endl;
}

void inicializaCirculo() {
    glGenVertexArrays(1, &Vao);
    glBindVertexArray(Vao);

    std::vector<float> vertices;
    int numFatias = 40; // Polígono 40 lados
    float raio = 1.0f; // Tamanho base normalizado
    float anguloIncremento = (2.0f * M_PI) / numFatias;

    // 1. Define o primeiro vértice na origem
    vertices.push_back(0.0f);
    vertices.push_back(0.0f);
    vertices.push_back(0.0f);

    // 2. Calcula os vértices da borda incrementando o ângulo usando seno e cosseno
    for (int i = 0; i <= numFatias; i++) {
        float angulo = i * anguloIncremento;
        vertices.push_back(raio * cos(angulo));
        vertices.push_back(raio * sin(angulo));
        vertices.push_back(0.0f);
    }

    GLuint pvbo;
    glGenBuffers(1, &pvbo);
    glBindBuffer(GL_ARRAY_BUFFER, pvbo);
    glBufferData(GL_ARRAY_BUFFER, vertices.size() * sizeof(float), vertices.data(), GL_STATIC_DRAW);
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, (void*)0);
}

void inicializaShaders() {
    // Vertex Shader
    const char* vertex_shader = 
        "#version 400\n"
        "layout(location = 0) in vec3 vertex_posicao;\n"
        "uniform mat4 model;\n" // Matriz combinada enviada pela aplicação
        "void main () {\n"
        "    // O vértice recebe a coordenada w=1.0 para viabilizar a translação\n"
        "    gl_Position = model * vec4(vertex_posicao, 1.0);\n" 
        "}\n";

    GLuint vs = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(vs, 1, &vertex_shader, NULL);
    glCompileShader(vs);
    
    GLint success;
    char infoLog[512];
    glGetShaderiv(vs, GL_COMPILE_STATUS, &success);
    if (!success) {
        glGetShaderInfoLog(vs, 512, NULL, infoLog);
        std::cerr << "Erro no vertex shader:\n" << infoLog << std::endl;
    }

    // Fragment Shader
    const char* fragment_shader = 
        "#version 400\n"
        "out vec4 frag_colour;\n"
        "uniform vec4 customColor;\n" // Variável uniform de cor
        "void main () {\n"
        "    frag_colour = customColor;\n" // Pintando todos os fragmentos com a mesma cor
        "}\n";

    GLuint fs = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(fs, 1, &fragment_shader, NULL);
    glCompileShader(fs);
    
    glGetShaderiv(fs, GL_COMPILE_STATUS, &success);
    if (!success) {
        glGetShaderInfoLog(fs, 512, NULL, infoLog);
        std::cerr << "Erro no fragment shader:\n" << infoLog << std::endl;
    }

    Shader_programm = glCreateProgram();
    glAttachShader(Shader_programm, vs);
    glAttachShader(Shader_programm, fs);
    glLinkProgram(Shader_programm);
    
    glGetProgramiv(Shader_programm, GL_LINK_STATUS, &success);
    if (!success) {
        glGetProgramInfoLog(Shader_programm, 512, NULL, infoLog);
        std::cerr << "Erro na linkagem do shader:\n" << infoLog << std::endl;
    }

    glDeleteShader(vs);
    glDeleteShader(fs);
}

void inicializaRenderizacao() {
    // Para o GL_TRIANGLE_FAN, o número de vértices é (fatias + 1 bordas + 1 origem)
    int numVertices = 40 + 2; 

    while (!glfwWindowShouldClose(Window)) {
        glClear(GL_COLOR_BUFFER_BIT);
        glClearColor(0.0f, 0.05f, 0.15f, 1.0f); // Fundo estilo espacial
        glViewport(0, 0, WIDTH, HEIGHT);

        // Parte 1: Ativa o programa de shader (obrigatório antes de enviar uniforms)
        glUseProgram(Shader_programm);
        glBindVertexArray(Vao);

        // Recupera a localização de memória das variáveis no shader para a matriz modelo e cor
        unsigned int modelLoc = glGetUniformLocation(Shader_programm, "model");
        int colorLoc = glGetUniformLocation(Shader_programm, "customColor");

        // ==========================================
        // Parte 2: Renderização do Astro Central
        // ==========================================
        glm::mat4 modelAstro = glm::mat4(1.0f);
        
        // Aplica escala para o sol (ocupará 30% da tela)
        modelAstro = glm::scale(modelAstro, glm::vec3(0.3f, 0.3f, 0.3f));
        
        glUniformMatrix4fv(modelLoc, 1, GL_FALSE, glm::value_ptr(modelAstro));

        // Envia a cor do astro
        glUniform4f(colorLoc, 1.0f, 0.2f, 0.5f, 1.0f);

        glDrawArrays(GL_TRIANGLE_FAN, 0, numVertices);

        // ==========================================
        // Parte 3: Renderização do Satélite em Órbita
        // ==========================================
        glm::mat4 modelSatelite = glm::mat4(1.0f);
        float tempo = (float)glfwGetTime();

        // Aplica estritamente na ordem solicitada de transformações: rotação, translação e escala
        
        // 1. Rotação (Roll - Eixo Z) para definir o ângulo atual da órbita
        modelSatelite = glm::rotate(modelSatelite, tempo, glm::vec3(0.0f, 0.0f, 1.0f));
        
        // 2. Translação para afastar o satélite da origem (Raio da órbita = 0.7)
        modelSatelite = glm::translate(modelSatelite, glm::vec3(0.7f, 0.0f, 0.0f)); 
        
        // 3. Escala para reduzir o tamanho do polígono (Satélite pequeno, S = 0.1)
        modelSatelite = glm::scale(modelSatelite, glm::vec3(0.1f, 0.1f, 0.1f));

        glUniformMatrix4fv(modelLoc, 1, GL_FALSE, glm::value_ptr(modelSatelite));

        // Envia a cor do satélite
        glUniform4f(colorLoc, 0.5f, 0.0f, 0.5f, 1.0f);

        glDrawArrays(GL_TRIANGLE_FAN, 0, numVertices);

        glfwPollEvents();
        glfwSwapBuffers(Window);

        if (glfwGetKey(Window, GLFW_KEY_ESCAPE) == GLFW_PRESS) {
            glfwSetWindowShouldClose(Window, true);
        }
    }
    
    glfwTerminate();
}

// Função principal
int main() {
    inicializaOpenGL();
    inicializaCirculo();
    inicializaShaders();
    inicializaRenderizacao();
    
    return 0;
}

#include <stdio.h>
#include <stdlib.h>

#define TRUE 1
#define FALSE 0

#define MAX_REGEX 512
#define MAX_INPUT 512
#define DEFAULT_GENERATION_LENGTH 6
#define MAX_GENERATION_LENGTH 10
#define SCREEN_WIDTH 80
#define INTEGRANTES "Blazquez, De la Vega, Rodriguez, Sandoval, Valdebenito."
#define PROJECT_TITLE "GENERADOR DE EXPRESIONES REGULARES"

typedef int Bool;

typedef enum {
    NODE_LITERAL,
    NODE_EPSILON,
    NODE_UNION,
    NODE_CONCAT,
    NODE_STAR
} NodeType;

/*
   Cada expresion regular se transforma en un arbol sintactico.
   El arbol permite resolver la generacion y la validacion.
*/
typedef struct Node {
    NodeType type;
    char value;
    struct Node *left;
    struct Node *right;
} Node;

typedef struct {
    const char *text;
    int pos;
    char error[180];
} Parser;

static int is_space(char c);
static int text_length(const char *text);
static int text_compare(const char *left, const char *right);
static Bool parse_non_negative_int(const char *text, int *value);
static void copy_text(char *destination, int destination_size, const char *source);
static void strip_newline(char *text);
static char *trim(char *text);
static void print_right_aligned(const char *text);
static void print_header(void);

static void set_error(Parser *parser, const char *message);
static void skip_spaces(Parser *parser);
static char current_char(Parser *parser);
static Bool is_binary_operator(char c);
static Bool is_reserved_char(char c);
static Bool starts_atom(char c);

static Node *new_node(NodeType type, char value, Node *left, Node *right);
static void free_tree(Node *node);
static Node *parse_atom(Parser *parser);
static Node *parse_postfix(Parser *parser);
static Node *parse_concat(Parser *parser);
static Node *parse_expression(Parser *parser);
static Node *parse_regex(const char *regex, char *error, int error_size);

static int *new_positions(int length);
static void clear_positions(int *positions, int length);
static void merge_positions(int *destination, const int *source, int length);
static void match_positions(const Node *node, const char *text, int length, int start, int *out);
static Bool accepts(const Node *root, const char *text);

static void sort_alphabet(char *alphabet, int count);
static void collect_alphabet(const char *regex, char *alphabet, int *count);
static void print_word(const char *word, int *printed, int *line_width);
static void generate_for_length(const Node *root, const char *alphabet, int alphabet_count,
                                int target_length, char *buffer, int depth,
                                int *printed, int *line_width);
static void generate_words(const Node *root, const char *alphabet, int alphabet_count, int max_length);

static int read_generation_length(void);
static void print_alphabet(const char *alphabet, int count);
static void print_help(void);
static void test_words(const Node *root);

static int is_space(char c) {
    return c == ' ' || c == '\t' || c == '\n' || c == '\r' || c == '\v' || c == '\f';
}

static int text_length(const char *text) {
    int length;

    length = 0;
    while (text[length] != '\0') {
        length++;
    }

    return length;
}

static int text_compare(const char *left, const char *right) {
    int i;

    i = 0;
    while (left[i] != '\0' && right[i] != '\0' && left[i] == right[i]) {
        i++;
    }

    return (unsigned char)left[i] - (unsigned char)right[i];
}

static Bool parse_non_negative_int(const char *text, int *value) {
    int i;
    int result;

    if (text[0] == '\0') {
        return FALSE;
    }

    result = 0;
    for (i = 0; text[i] != '\0'; i++) {
        if (text[i] < '0' || text[i] > '9') {
            return FALSE;
        }
        result = result * 10 + (text[i] - '0');
    }

    *value = result;
    return TRUE;
}

static void copy_text(char *destination, int destination_size, const char *source) {
    int i;

    if (destination_size == 0) {
        return;
    }

    i = 0;
    while (source[i] != '\0' && i < destination_size - 1) {
        destination[i] = source[i];
        i++;
    }

    destination[i] = '\0';
}

static void strip_newline(char *text) {
    int i;

    i = 0;
    while (text[i] != '\0') {
        if (text[i] == '\r' || text[i] == '\n') {
            text[i] = '\0';
            return;
        }
        i++;
    }
}

static char *trim(char *text) {
    char *end;

    while (is_space(*text)) {
        text++;
    }

    if (*text == '\0') {
        return text;
    }

    end = text + text_length(text) - 1;
    while (end > text && is_space(*end)) {
        *end = '\0';
        end--;
    }

    return text;
}

static void print_right_aligned(const char *text) {
    int spaces;
    int i;
    int length;

    length = text_length(text);
    spaces = SCREEN_WIDTH - length;
    if (spaces < 0) {
        spaces = 0;
    }

    for (i = 0; i < spaces; i++) {
        printf(" ");
    }
    printf("%s\n", text);
}

static void print_header(void) {
    print_right_aligned(INTEGRANTES);
    printf("%s\n", PROJECT_TITLE);
    printf("============================================================\n");
    printf("Objetivo del programa:\n");
    printf("  1. Ingresar una expresion regular con union, concatenacion\n");
    printf("     y cerradura de Kleene.\n");
    printf("  2. Generar las cadenas aceptadas hasta una longitud maxima.\n");
    printf("  3. Probar cadenas ingresadas por el usuario e indicar si\n");
    printf("     pertenecen o no al lenguaje de la expresion.\n\n");
}

static void set_error(Parser *parser, const char *message) {
    if (parser->error[0] == '\0') {
        copy_text(parser->error, sizeof(parser->error), message);
    }
}

static void skip_spaces(Parser *parser) {
    while (is_space(parser->text[parser->pos])) {
        parser->pos++;
    }
}

static char current_char(Parser *parser) {
    skip_spaces(parser);
    return parser->text[parser->pos];
}

static Bool is_binary_operator(char c) {
    return c == '|' || c == '+' || c == '.';
}

static Bool is_reserved_char(char c) {
    return c == '\0' || c == '(' || c == ')' || c == '*' || is_binary_operator(c);
}

static Bool starts_atom(char c) {
    return c != '\0' && c != ')' && c != '|' && c != '+' && c != '.' && c != '*';
}

static Node *new_node(NodeType type, char value, Node *left, Node *right) {
    Node *node;

    node = (Node *)malloc(sizeof(Node));
    if (node == NULL) {
        fprintf(stderr, "No se pudo reservar memoria.\n");
        exit(1);
    }

    node->type = type;
    node->value = value;
    node->left = left;
    node->right = right;
    return node;
}

static void free_tree(Node *node) {
    if (node == NULL) {
        return;
    }

    free_tree(node->left);
    free_tree(node->right);
    free(node);
}

/*
   Analizador recursivo descendente:
   - parse_expression resuelve union.
   - parse_concat resuelve concatenacion.
   - parse_postfix resuelve cerradura de Kleene.
   - parse_atom resuelve simbolos, epsilon y parentesis.
*/
static Node *parse_atom(Parser *parser) {
    char c;
    Node *inside;

    c = current_char(parser);

    if (c == '(') {
        parser->pos++;
        inside = parse_expression(parser);
        if (inside == NULL) {
            return NULL;
        }

        if (current_char(parser) != ')') {
            free_tree(inside);
            set_error(parser, "Falta cerrar un parentesis.");
            return NULL;
        }

        parser->pos++;
        return inside;
    }

    if (c == 'E') {
        parser->pos++;
        return new_node(NODE_EPSILON, '\0', NULL, NULL);
    }

    if (is_reserved_char(c)) {
        set_error(parser, "Se esperaba un simbolo, E o un grupo entre parentesis.");
        return NULL;
    }

    parser->pos++;
    return new_node(NODE_LITERAL, c, NULL, NULL);
}

static Node *parse_postfix(Parser *parser) {
    Node *node;

    node = parse_atom(parser);
    if (node == NULL) {
        return NULL;
    }

    while (current_char(parser) == '*') {
        parser->pos++;
        node = new_node(NODE_STAR, '\0', node, NULL);
    }

    return node;
}

static Node *parse_concat(Parser *parser) {
    Node *left;
    Node *right;
    char c;

    left = parse_postfix(parser);
    if (left == NULL) {
        return NULL;
    }

    while (TRUE) {
        c = current_char(parser);

        if (c == '.') {
            parser->pos++;
        } else if (!starts_atom(c)) {
            break;
        }

        right = parse_postfix(parser);
        if (right == NULL) {
            free_tree(left);
            return NULL;
        }

        left = new_node(NODE_CONCAT, '\0', left, right);
    }

    return left;
}

static Node *parse_expression(Parser *parser) {
    Node *left;
    Node *right;
    char c;

    left = parse_concat(parser);
    if (left == NULL) {
        return NULL;
    }

    while (TRUE) {
        c = current_char(parser);
        if (c != '|' && c != '+') {
            break;
        }

        parser->pos++;
        right = parse_concat(parser);
        if (right == NULL) {
            free_tree(left);
            return NULL;
        }

        left = new_node(NODE_UNION, '\0', left, right);
    }

    return left;
}

static Node *parse_regex(const char *regex, char *error, int error_size) {
    Parser parser;
    Node *root;
    char message[180];

    parser.text = regex;
    parser.pos = 0;
    parser.error[0] = '\0';

    root = parse_expression(&parser);
    if (root == NULL) {
        copy_text(error, error_size, parser.error);
        return NULL;
    }

    if (current_char(&parser) != '\0') {
        free_tree(root);
        sprintf(message, "Caracter inesperado: '%c'.", current_char(&parser));
        copy_text(error, error_size, message);
        return NULL;
    }

    error[0] = '\0';
    return root;
}

static int *new_positions(int length) {
    int *positions;
    int i;

    positions = (int *)malloc((length + 1) * sizeof(int));
    if (positions == NULL) {
        fprintf(stderr, "No se pudo reservar memoria.\n");
        exit(1);
    }

    for (i = 0; i <= length; i++) {
        positions[i] = FALSE;
    }

    return positions;
}

static void clear_positions(int *positions, int length) {
    int i;

    for (i = 0; i <= length; i++) {
        positions[i] = FALSE;
    }
}

static void merge_positions(int *destination, const int *source, int length) {
    int i;

    for (i = 0; i <= length; i++) {
        if (source[i]) {
            destination[i] = TRUE;
        }
    }
}

/*
   Para cada nodo del arbol, se calculan las posiciones de la cadena a las que se puede llegar.
   Si desde la posicion 0 se puede llegar al final, la cadena es aceptada.
*/
static void match_positions(const Node *node, const char *text, int length, int start, int *out) {
    int *left_positions;
    int *right_positions;
    int *middle_positions;
    int *next_positions;
    int *queue;
    int head;
    int tail;
    int position;
    int i;

    clear_positions(out, length);

    if (start < 0 || start > length || node == NULL) {
        return;
    }

    if (node->type == NODE_LITERAL) {
        if (start < length && text[start] == node->value) {
            out[start + 1] = TRUE;
        }
        return;
    }

    if (node->type == NODE_EPSILON) {
        out[start] = TRUE;
        return;
    }

    if (node->type == NODE_UNION) {
        left_positions = new_positions(length);
        right_positions = new_positions(length);

        match_positions(node->left, text, length, start, left_positions);
        match_positions(node->right, text, length, start, right_positions);
        merge_positions(out, left_positions, length);
        merge_positions(out, right_positions, length);

        free(left_positions);
        free(right_positions);
        return;
    }

    if (node->type == NODE_CONCAT) {
        middle_positions = new_positions(length);
        right_positions = new_positions(length);

        match_positions(node->left, text, length, start, middle_positions);
        for (i = 0; i <= length; i++) {
            if (middle_positions[i]) {
                match_positions(node->right, text, length, i, right_positions);
                merge_positions(out, right_positions, length);
            }
        }

        free(middle_positions);
        free(right_positions);
        return;
    }

    if (node->type == NODE_STAR) {
        queue = (int *)malloc((length + 1) * sizeof(int));
        next_positions = new_positions(length);
        if (queue == NULL) {
            fprintf(stderr, "No se pudo reservar memoria.\n");
            exit(1);
        }

        head = 0;
        tail = 0;
        out[start] = TRUE;
        queue[tail] = start;
        tail++;

        /*
           Para Kleene se hace un recorrido por amplitud sobre posiciones.
           Asi se contemplan cero, una o muchas repeticiones sin caer en
           ciclos infinitos cuando la subexpresion acepta epsilon.
        */
        while (head < tail) {
            position = queue[head];
            head++;

            match_positions(node->left, text, length, position, next_positions);
            for (i = 0; i <= length; i++) {
                if (next_positions[i] && !out[i]) {
                    out[i] = TRUE;
                    queue[tail] = i;
                    tail++;
                }
            }
        }

        free(queue);
        free(next_positions);
    }
}

static Bool accepts(const Node *root, const char *text) {
    int length;
    int *positions;
    Bool result;

    length = text_length(text);
    positions = new_positions(length);
    match_positions(root, text, length, 0, positions);
    result = positions[length] ? TRUE : FALSE;

    free(positions);
    return result;
}

static void sort_alphabet(char *alphabet, int count) {
    int i;
    int j;
    char aux;

    for (i = 0; i < count - 1; i++) {
        for (j = 0; j < count - i - 1; j++) {
            if (alphabet[j] > alphabet[j + 1]) {
                aux = alphabet[j];
                alphabet[j] = alphabet[j + 1];
                alphabet[j + 1] = aux;
            }
        }
    }
}

static void collect_alphabet(const char *regex, char *alphabet, int *count) {
    int i;
    int j;
    char c;
    Bool repeated;

    *count = 0;
    for (i = 0; regex[i] != '\0'; i++) {
        c = regex[i];
        repeated = FALSE;

        if (is_space(c) || is_reserved_char(c) || c == 'E') {
            continue;
        }

        for (j = 0; j < *count; j++) {
            if (alphabet[j] == c) {
                repeated = TRUE;
                break;
            }
        }

        if (!repeated) {
            alphabet[*count] = c;
            (*count)++;
        }
    }

    sort_alphabet(alphabet, *count);
}

static void print_word(const char *word, int *printed, int *line_width) {
    const char *shown;
    int extra;

    shown = word[0] == '\0' ? "E" : word;
    extra = text_length(shown) + (*printed > 0 ? 2 : 0);

    if (*printed > 0) {
        printf(",");
    }

    if (*line_width + extra > 100) {
        printf("\n  ");
        *line_width = 2;
    } else if (*printed > 0) {
        printf(" ");
        *line_width += 2;
    }

    printf("%s", shown);
    *line_width += text_length(shown);
    (*printed)++;
}

/*
   Generacion clasica:
   se enumeran todas las cadenas posibles del alfabeto detectado,
   desde longitud 0 hasta la longitud maxima. Luego se conserva solo
   cada cadena que el arbol de la expresion acepta.
*/
static void generate_for_length(const Node *root, const char *alphabet, int alphabet_count,
                                int target_length, char *buffer, int depth,
                                int *printed, int *line_width) {
    int i;

    if (depth == target_length) {
        buffer[depth] = '\0';
        if (accepts(root, buffer)) {
            print_word(buffer, printed, line_width);
        }
        return;
    }

    if (alphabet_count == 0) {
        return;
    }

    for (i = 0; i < alphabet_count; i++) {
        buffer[depth] = alphabet[i];
        generate_for_length(root, alphabet, alphabet_count, target_length, buffer, depth + 1,
                            printed, line_width);
    }
}

static void generate_words(const Node *root, const char *alphabet, int alphabet_count, int max_length) {
    int length;
    int printed;
    int line_width;
    char buffer[MAX_GENERATION_LENGTH + 1];

    printed = 0;
    line_width = 2;

    printf("\nCadenas generadas hasta longitud %d:\n{ ", max_length);
    for (length = 0; length <= max_length; length++) {
        generate_for_length(root, alphabet, alphabet_count, length, buffer, 0, &printed, &line_width);
    }

    if (printed == 0) {
        printf("No se encontraron cadenas con esa longitud maxima");
    }

    printf(" }\n");
}

static int read_generation_length(void) {
    char line[MAX_INPUT];
    char *clean;
    int value;

    printf("Longitud maxima a generar [default %d, max %d]: ",
           DEFAULT_GENERATION_LENGTH, MAX_GENERATION_LENGTH);

    if (fgets(line, sizeof(line), stdin) == NULL) {
        return DEFAULT_GENERATION_LENGTH;
    }

    strip_newline(line);
    clean = trim(line);

    if (clean[0] == '\0') {
        return DEFAULT_GENERATION_LENGTH;
    }

    if (!parse_non_negative_int(clean, &value)) {
        printf("Valor invalido. Se usara %d.\n", DEFAULT_GENERATION_LENGTH);
        return DEFAULT_GENERATION_LENGTH;
    }

    if (value > MAX_GENERATION_LENGTH) {
        printf("La longitud se limito a %d para evitar demasiadas combinaciones.\n",
               MAX_GENERATION_LENGTH);
        value = MAX_GENERATION_LENGTH;
    }

    return value;
}

static void print_alphabet(const char *alphabet, int count) {
    int i;

    printf("Alfabeto detectado: {");
    if (count == 0) {
        printf(" }");
    } else {
        for (i = 0; i < count; i++) {
            printf("%s%c", i == 0 ? " " : ", ", alphabet[i]);
        }
        printf(" }");
    }
    printf("\n");
}

static void print_help(void) {
    printf("Operadores permitidos:\n");
    printf("  .  concatenacion explicita\n");
    printf("  |  union\n");
    printf("  +  union\n");
    printf("  *  cerradura de Kleene\n");
    printf("  () agrupacion\n");
    printf("  E  cadena vacia epsilon\n\n");
    printf("Reglas de uso:\n");
    printf("  - No usar espacios como simbolos del alfabeto.\n");
    printf("  - La letra E queda reservada para representar epsilon.\n");
    printf("  - Se acepta concatenacion explicita con punto: a.b\n");
    printf("  - Tambien se acepta concatenacion implicita: ab\n\n");
    printf("Ejemplos validos:\n");
    printf("  a.b*\n");
    printf("  (a|b)*.a\n");
    printf("  a.(b|c)\n");
    printf("  (a|E).b\n\n");
}

static void test_words(const Node *root) {
    char line[MAX_INPUT];
    char *word;

    printf("\nAhora pruebe cadenas.\n");
    printf("Escriba salir para terminar con esta ER.\n");
    printf("Use E o una linea vacia para probar la cadena vacia.\n\n");

    while (TRUE) {
        printf("Cadena a probar: ");
        if (fgets(line, sizeof(line), stdin) == NULL) {
            printf("\n");
            return;
        }

        strip_newline(line);
        word = trim(line);

        if (text_compare(word, "salir") == 0) {
            return;
        }

        if (text_compare(word, "E") == 0) {
            word[0] = '\0';
        }

        printf("Resultado: %s\n", accepts(root, word) ? "ACEPTADA" : "RECHAZADA");
    }
}

int main(void) {
    char line[MAX_REGEX];
    char *regex;
    char error[180];
    char alphabet[MAX_REGEX];
    int alphabet_count;
    int max_length;
    Node *root;

    print_header();
    print_help();

    while (TRUE) {
        printf("Ingrese una expresion regular (o salir): ");
        if (fgets(line, sizeof(line), stdin) == NULL) {
            printf("\n");
            break;
        }

        strip_newline(line);
        regex = trim(line);

        if (text_compare(regex, "salir") == 0) {
            break;
        }

        if (regex[0] == '\0') {
            printf("Debe ingresar una expresion regular.\n\n");
            continue;
        }

        root = parse_regex(regex, error, sizeof(error));
        if (root == NULL) {
            printf("Error en la expresion: %s\n\n", error);
            continue;
        }

        collect_alphabet(regex, alphabet, &alphabet_count);
        print_alphabet(alphabet, alphabet_count);
        max_length = read_generation_length();
        generate_words(root, alphabet, alphabet_count, max_length);
        test_words(root);
        free_tree(root);

        printf("\n");
    }

    printf("Programa finalizado.\n");
    return 0;
}

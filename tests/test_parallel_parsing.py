import multiprocessing
import os
import sys
from antlr4 import FileStream, CommonTokenStream

# Add UFC directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ufc'))

from frontend.c.parser.frontend.c._antlr.CLexer import CLexer
from frontend.c.parser.frontend.c._antlr.CParser import CParser
from frontend.cpp.parser.CPP14Lexer import CPP14Lexer
from frontend.cpp.parser.CPP14Parser import CPP14Parser
from frontend.java.parser.Java9Lexer import Java9Lexer
from frontend.java.parser.Java9Parser import Java9Parser

def parse_c_file(file_path):
    try:
        input_stream = FileStream(file_path)
        lexer = CLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = CParser(stream)
        tree = parser.compilationUnit()
        return True
    except Exception as e:
        print(f"Error parsing C file: {e}")
        return False

def parse_cpp_file(file_path):
    try:
        input_stream = FileStream(file_path)
        lexer = CPP14Lexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = CPP14Parser(stream)
        tree = parser.translationUnit()
        return True
    except Exception as e:
        print(f"Error parsing C++ file: {e}")
        return False

def parse_java_file(file_path):
    try:
        input_stream = FileStream(file_path)
        lexer = Java9Lexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = Java9Parser(stream)
        tree = parser.compilationUnit()
        return True
    except Exception as e:
        print(f"Error parsing Java file: {e}")
        return False

def test_parallel_parsing():
    # Create test files
    test_files = {
        'c_test.c': '''
            int main() {
                return 0;
            }
        ''',
        'cpp_test.cpp': '''
            int main() {
                return 0;
            }
        ''',
        'java_test.java': '''
            public class Test {
                public static void main(String[] args) {
                    System.out.println("Hello");
                }
            }
        '''
    }

    # Get absolute path for samples directory
    samples_dir = os.path.join(os.path.dirname(__file__), 'samples')
    os.makedirs(samples_dir, exist_ok=True)

    # Write test files
    for filename, content in test_files.items():
        with open(os.path.join(samples_dir, filename), 'w') as f:
            f.write(content)

    # Create a pool of workers
    with multiprocessing.Pool(processes=3) as pool:
        # Prepare parsing tasks with absolute paths
        tasks = [
            (parse_c_file, os.path.join(samples_dir, 'c_test.c')),
            (parse_cpp_file, os.path.join(samples_dir, 'cpp_test.cpp')),
            (parse_java_file, os.path.join(samples_dir, 'java_test.java'))
        ]

        # Execute parsing in parallel
        results = [pool.apply_async(func, (file_path,)) for func, file_path in tasks]

        # Get results and verify all files parsed successfully
        parsed_results = [result.get() for result in results]

        # Verify results - all parsing operations should return True
        assert all(parsed_results), "One or more files failed to parse"

if __name__ == '__main__':
    test_parallel_parsing()

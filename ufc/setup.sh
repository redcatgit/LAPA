#!/bin/bash

# Exit on any error
set -e

echo "Cleaning up existing parser files..."
rm -rf frontend/c/parser/* frontend/cpp/parser/* frontend/java/parser/*

echo "Downloading ANTLR grammars..."

# Create directories if they don't exist
mkdir -p frontend/c/_antlr frontend/cpp/_antlr frontend/java/_antlr frontend/c/parser frontend/cpp/parser frontend/java/parser

# Download ANTLR grammars
wget https://raw.githubusercontent.com/antlr/grammars-v4/master/c/C.g4 -O frontend/c/_antlr/C.g4
wget https://raw.githubusercontent.com/antlr/grammars-v4/master/cpp/CPP14Lexer.g4 -O frontend/cpp/_antlr/CPP14Lexer.g4
wget https://raw.githubusercontent.com/antlr/grammars-v4/master/cpp/CPP14Parser.g4 -O frontend/cpp/_antlr/CPP14Parser.g4
wget https://raw.githubusercontent.com/antlr/grammars-v4/master/java/java9/Java9Lexer.g4 -O frontend/java/_antlr/Java9Lexer.g4
wget https://raw.githubusercontent.com/antlr/grammars-v4/master/java/java9/Java9Parser.g4 -O frontend/java/_antlr/Java9Parser.g4

echo "Generating parsers..."

# Generate parsers with specific ANTLR version
# C Parser
antlr4 -Dlanguage=Python3 -visitor frontend/c/_antlr/C.g4 -o frontend/c/parser

# C++ Parser
cd frontend/cpp/_antlr
antlr4 -Dlanguage=Python3 -visitor CPP14Lexer.g4 CPP14Parser.g4 -o ../parser
cd ../../..

# Java Parser
cd frontend/java/_antlr
antlr4 -Dlanguage=Python3 -visitor Java9Lexer.g4 Java9Parser.g4 -o ../parser
cd ../../..

echo "Setup completed successfully!"

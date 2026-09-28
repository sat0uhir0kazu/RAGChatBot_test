"""
ドキュメントローダーモジュール
PDF、DOCX、TXT、MDファイルのドキュメント読み込み
"""

import os
from typing import List
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader
)
from langchain_core.documents import Document


class DocumentLoader:
    """様々な形式のドキュメントを読み込むクラス"""

    def __init__(self):
        self.supported_extensions = {
            ".pdf": PyPDFLoader,
            ".docx": Docx2txtLoader,
            ".txt": TextLoader,
            ".md": TextLoader
        }

    def load_file(self, file_path: str) -> List[Document]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")

        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        if ext not in self.supported_extensions:
            raise ValueError(f"サポートされていないファイル形式: {ext}")

        try:
            loader_class = self.supported_extensions[ext]

            if ext in [".txt", ".md"]:
                try:
                    loader = loader_class(file_path, encoding="utf-8")
                    documents = loader.load()
                except Exception:
                    loader = loader_class(file_path, encoding="cp932")
                    documents = loader.load()
            else:
                loader = loader_class(file_path)
                documents = loader.load()

            for doc in documents:
                doc.metadata["source"] = os.path.basename(file_path)

            return documents

        except Exception as e:
            raise Exception(f"ファイル読み込みエラー: {str(e)}")

    def load_directory(self, directory_path: str) -> List[Document]:
        if not os.path.exists(directory_path):
            raise FileNotFoundError(f"ディレクトリが見つかりません: {directory_path}")

        all_documents = []

        for filename in sorted(os.listdir(directory_path)):
            file_path = os.path.join(directory_path, filename)

            if os.path.isdir(file_path):
                continue

            _, ext = os.path.splitext(filename)

            if ext.lower() in self.supported_extensions:
                try:
                    documents = self.load_file(file_path)
                    all_documents.extend(documents)
                except Exception as e:
                    print(f"読み込み失敗: {file_path}")
                    print(f"理由: {e}")

        return all_documents

    def load_files(self, file_paths: List[str]) -> List[Document]:
        all_documents = []

        for file_path in file_paths:
            try:
                documents = self.load_file(file_path)
                all_documents.extend(documents)
            except Exception as e:
                print(f"読み込み失敗: {file_path}")
                print(f"理由: {e}")

        return all_documents
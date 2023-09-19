# pygptprompt/database/document.py
#
# Copyright 2023 PromtEngineer/localGPT
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging
import os
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from typing import List, Tuple

from pygptprompt import CPU_COUNT


def load_single_document(file_path: str) -> Document:
    """
    Loads a single document from the given file path.

    Args:
        file_path (str): The path to the document file.

    Returns:
        Document: The loaded document.

    Raises:
        ValueError: If the document type is undefined.
    """
    mime_type = loader_registry.get_mime_type(file_path)
    cls_DocumentLoader = loader_registry.get_loader(mime_type)
    if cls_DocumentLoader:
        loader = cls_DocumentLoader(file_path)
    else:
        raise ValueError(f"Document type is undefined: {mime_type}")
    return loader.load()[0]


def load_document_batch(
    filepaths: List[str],
) -> Tuple[List[Document], List[str]]:
    """
    Loads a batch of documents from the given file paths.

    Args:
        filepaths (List[str]): List of file paths to load the documents from.

    Returns:
        Tuple[List[Document], List[str]]: A tuple containing the loaded documents and
        the corresponding file paths.

    Raises:
        ValueError: If the document type is undefined.
    """
    logging.info("Loading document batch")
    # create a thread pool
    with ThreadPoolExecutor(len(filepaths)) as exe:
        # load files
        futures = [exe.submit(load_single_document, path) for path in filepaths]
        # collect data
        data_list = [future.result() for future in futures]
        # return data and file paths
        return (data_list, filepaths)


def load_documents(source_dir: str) -> List[Document]:
    """
    Loads all documents from the specified source documents directory.

    Args:
        source_dir (str): The path to the source documents directory.

    Returns:
        List[Document]: A list of loaded documents.

    Raises:
        ValueError: If the document type is undefined.
    """
    paths = []
    all_files = os.listdir(source_dir)

    logging.info(f"Loading documents: {source_dir}")
    logging.info(f"Loading document files: {all_files}")

    for file_path in all_files:
        source_file_path = os.path.join(source_dir, file_path)
        mime_type = loader_registry.get_mime_type(source_file_path)
        loader_class = loader_registry.get_loader(mime_type)

        logging.info(f"Detected {mime_type} for {file_path}")

        if loader_class:
            logging.info(f"Loading {source_file_path}")
            paths.append(source_file_path)

    # Have at least one worker and at most INGEST_THREADS workers
    n_workers = min(CPU_COUNT, max(len(paths), 1))
    chunk_size = round(len(paths) / n_workers)
    docs = []

    with ProcessPoolExecutor(n_workers) as executor:
        futures = []
        # split the load operations into chunks
        for i in range(0, len(paths), chunk_size):
            # select a chunk of filenames
            filepaths = paths[i : (i + chunk_size)]
            # submit the task
            future = executor.submit(load_document_batch, filepaths)
            futures.append(future)
        # process all results
        for future in as_completed(futures):
            # open the file and load the data
            contents, _ = future.result()
            docs.extend(contents)

    return docs

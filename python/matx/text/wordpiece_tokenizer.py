# Copyright 2022 ByteDance Ltd. and/or its affiliates.
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from typing import List, Tuple, AnyStr, Any

from .._ffi.base import load_lib_by_name
from ..native._native_object import make_native_object

_LIB, _LIB_NAME, _LIB_SHA1 = load_lib_by_name("libmatx_text_ops")


class WordPieceTokenizer(object):

    def __init__(self,
                 vocab_path: str,
                 lookup_id: bool = True,
                 unk_token: Any = "[UNK]",
                 subwords_prefix: str = "##",
                 skip_empty: bool = True,
                 max_bytes_per_token: int = 100,
                 ) -> None:
        self.tokenizer: Any = make_native_object(
            "text_tokenizer_WordPieceTokenizer",
            vocab_path,
            lookup_id,
            unk_token,
            subwords_prefix,
            skip_empty,
            max_bytes_per_token,
        )

    def __call__(self, sentence: List[AnyStr]) -> List[AnyStr]:
        return self.tokenizer.tokenize(sentence)


class WordPieceTokenizerWithMeta(object):

    def __init__(self,
                 vocab_path: str,
                 lookup_id: bool = True,
                 unk_token: Any = "[UNK]",
                 subwords_prefix: str = "##",
                 skip_empty: bool = True,
                 max_bytes_per_token: int = 100,
                 ) -> None:
        self.tokenizer: Any = make_native_object(
            "text_tokenizer_WordPieceTokenizer",
            vocab_path,
            lookup_id,
            unk_token,
            subwords_prefix,
            skip_empty,
            max_bytes_per_token,
        )

    def __call__(self, sentence: List[AnyStr]) -> Tuple[List[AnyStr], List[int]]:
        return self.tokenizer.tokenize_with_meta(sentence)

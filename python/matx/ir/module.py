# Copyright 2022 ByteDance Ltd. and/or its affiliates.
#
# Acknowledgement: The structure of the IRModule is inspired by incubator-tvm.
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
"""IRModule that holds the functions and type definitions."""
from .._ffi.base import string_types
from .. import _ffi

from .base import Node
from . import expr as _expr
from . import type as _ty
from . import _ffi_api
from ._converter import to_ir_object as _to_ir


@_ffi.register_object("IRModule")
class IRModule(Node):
    """IRModule that holds functions and type definitions.

    IRModule is the basic unit for all IR transformations across the stack.

    Parameters
    ----------
    functions: Optional[dict].
        Map of global var to BaseFunc

    type_definitions: Optional[Dict[GlobalTypeVar, Type]]
        Map of global type var to ClsasType

    """

    def __init__(self, functions=None, type_definitions=None):
        if functions is None:
            functions = {}
        elif isinstance(functions, dict):
            mapped_funcs = {}
            for k, v in functions.items():
                if isinstance(k, string_types):
                    k = _expr.GlobalVar(k)
                if not isinstance(k, _expr.GlobalVar):
                    raise TypeError("Expect functions to be Dict[GlobalVar, Function]")
                mapped_funcs[k] = v
            functions = mapped_funcs
        if type_definitions is None:
            type_definitions = {}
        elif isinstance(type_definitions, dict):
            mapped_type_defs = {}
            for k, v in type_definitions.items():
                if isinstance(k, string_types):
                    k = _ty.GlobalTypeVar(k)
                if not isinstance(k, _ty.GlobalTypeVar):
                    raise TypeError("Expect type_definitions to be Dict[GlobalTypeVar, Type]")
                mapped_type_defs[k] = v
            type_definitions = mapped_type_defs
        self.__init_handle_by_constructor__(_ffi_api.IRModule,
                                            _to_ir(functions),
                                            _to_ir(type_definitions))

    def __setitem__(self, var, val):
        """Add a mapping to the module.

        Parameters
        ---------
        var: GlobalVar
            The global variable.

        val: Union[Function, Type]
            The value.
        """
        return self._add(var, _to_ir(val), True)

    def _add(self, var, val, update=True):
        if isinstance(val, _expr.HLOExpr):
            if isinstance(var, string_types):
                var = var.encode("utf-8")
                if _ffi_api.Module_ContainGlobalVar(self, var):
                    var = _ffi_api.Module_GetGlobalVar(self, var)
                else:
                    var = _expr.GlobalVar(var)
            _ffi_api.Module_Add(self, var, val, update)
        else:
            assert isinstance(val, _ty.Type)
            if isinstance(var, string_types):
                var = _ty.GlobalTypeVar(var)
            _ffi_api.Module_AddDef(self, var, val, update)

    def __getitem__(self, var):
        """Lookup a global definition by name or by variable.

        Parameters
        ----------
        var: Union[String, GlobalVar, GlobalTypeVar]
            The name or global variable.

        Returns
        -------
        val: Union[Function, Type]
            The definition referenced by :code:`var` (either a function or type).
        """
        if isinstance(var, string_types):
            return _ffi_api.Module_Lookup_str(self, _to_ir(var))
        if isinstance(var, _expr.GlobalVar):
            return _ffi_api.Module_Lookup(self, var)
        return _ffi_api.Module_LookupDef(self, var)

    def update(self, other):
        """Insert functions in another Module to current one.

        Parameters
        ----------
        other: IRModule
            The module to merge into the current Module.
        """
        if isinstance(other, dict):
            other = IRModule(other)

        return _ffi_api.Module_Update(self, other)

    def update_func(self, var, func):
        """Update the function corresponding to a global variable in the
        module.

        Parameters
        ----------
        var: GlobalVar
            The global variable.

        func: tvm.relay.Function
            The function to be inserted.
        """
        return _ffi_api.Module_UpdateFunction(self, _to_ir(var), func)

    def add_export_func(self, export_func):
        return _ffi_api.Module_AddExportFunction(self, export_func)

    def set_main(self, main):
        self.add_export_func(main)

    def get_global_var(self, name):
        """Get a global variable in the function by name.

        Parameters
        ----------
        name: str
            The name of the global variable.

        Returns
        -------
        global_var: GlobalVar
            The global variable mapped to :code:`name`.

        Raises
        ------
        tvm.error.TVMError if we cannot find corresponding global var.
        """
        return _ffi_api.Module_GetGlobalVar(self, _to_ir(name))

    def get_global_vars(self):
        """Collect all global vars defined in this module.

        Returns
        -------
        global_vars: Array[GlobalVar]
            An array of global vars.
        """
        return _ffi_api.Module_GetGlobalVars(self)

    def get_global_type_vars(self):
        """Collect all global type vars defined in this module.

        Returns
        -------
        global_type_vars: Array[GlobalTypeVar]
            An array of global type vars.
        """
        return _ffi_api.Module_GetGlobalTypeVars(self)

    def get_global_type_var(self, name):
        """Get a global type variable in the function by name.

        Parameters
        ----------
        name: str
            The name of the global type variable.

        Returns
        -------
        global_type_var: GlobalTypeVar
            The global variable mapped to :code:`name`.

        Raises
        ------
        tvm.error.TVMError if we cannot find corresponding global type var.
        """
        return _ffi_api.Module_GetGlobalTypeVar(self, _to_ir(name))

    def get_type(self, name):
        ty_var = self.get_global_type_var(name)
        ty_data = self.type_definitions[ty_var]
        return tuple([ty_var] + list(ty_data.constructors))

    @staticmethod
    def from_expr(expr, functions=None, type_defs=None):
        """Construct a module from a standalone expression.

        Parameters
        ----------
        expr: RelayExpr
            The starting expression

        global_funcs: Optional[dict]
            Map of global vars to function definitions

        type_defs: Optional[dict]
            Map of global type vars to type definitions

        Returns
        -------
        mod: Module
            A module containing the passed definitions,
            where expr is set as the entry point
            (wrapped in a function if necessary)
        """
        funcs = functions if functions is not None else {}
        defs = type_defs if type_defs is not None else {}
        return _ffi_api.Module_FromExpr(expr, _to_ir(funcs), _to_ir(defs))

    def __str__(self):
        # TODO(jroesch): why does this hang sometimes?
        return self.astext()

    def __repr__(self):
        return self.astext()

1. Iterate over each APK
2. Decompile each APK
3. Iterate over each .java file
4. Iterate over method in the .java file
5. For each method, create a json object containing the following fields:
   - id = unique identifier
   - mongo_id = unique identifier
   - md5 = md5 hash of the function
   - func_name = name of the function
   - func = the implementation of the function
   - norm_func = the implementation of the function, where the names of the variables have been normalized. Java variable names are formatted in CamelCase. Hence, normalization means splitting names and put a lower dash where from lower case we move to upper case. Then, we lowercase the resulting string.
   - var = the list of variable names
   - vars_map = a list of sublists, where each sublist contains 2 elements: the first element is the original variable name, while the second element is the normalized variable name.

I give you an example. Given this function:

enum winbindd_result winbindd_dual_init_connection(struct winbindd_domain *@@var_1@@domain@@,\n\t\t\t\t\t\t   struct winbindd_cli_state *@@var_3@@state@@)\n{\n\t\n\t@@var_3@@state@@->request->domain_name\n\t\t[sizeof(@@var_3@@state@@->request->domain_name)-1]='\\0';\n\t@@var_3@@state@@->request->data.init_conn.dcname\n\t\t[sizeof(@@var_3@@state@@->request->data.init_conn.dcname)-1]='\\0';\n\n\tif (strlen(@@var_3@@state@@->request->data.init_conn.dcname) > 0) {\n\t\tTALLOC_FREE(@@var_1@@domain@@->dcname);\n\t\t@@var_1@@domain@@->dcname = talloc_strdup(@@var_1@@domain@@,\n\t\t\t\t@@var_3@@state@@->request->data.init_conn.dcname);\n\t\tif (@@var_1@@domain@@->dcname == NULL) {\n\t\t\treturn @@var_4@@WINBINDD_ERROR@@;\n\t\t}\n\t}\n\n\tinit_dc_connection(@@var_1@@domain@@, (0));\n\n\tif (!@@var_1@@domain@@->initialized) {\n\t\t\n\t\tDEBUG(5, (\"winbindd_dual_init_connection: %s returning without initialization \"\n\t\t\t\"online = %d\\n\", @@var_1@@domain@@->name, (int)@@var_1@@domain@@->online ));\n\t}\n\n\tfstrcpy(@@var_3@@state@@->response->data.domain_info.name, @@var_1@@domain@@->name);\n\tfstrcpy(@@var_3@@state@@->response->data.domain_info.alt_name, @@var_1@@domain@@->alt_name);\n\tsid_to_fstring(@@var_3@@state@@->response->data.domain_info.sid, &@@var_1@@domain@@->sid);\n\n\t@@var_3@@state@@->response->data.domain_info.native_mode\n\t\t= @@var_1@@domain@@->native_mode;\n\t@@var_3@@state@@->response->data.domain_info.active_directory\n\t\t= @@var_1@@domain@@->active_directory;\n\t@@var_3@@state@@->response->data.domain_info.primary\n\t\t= @@var_1@@domain@@->primary;\n\n\treturn @@var_2@@WINBINDD_OK@@;\n}

The output json should look as the following:

{
   "id":4586685,
   "mongo_id":"5fddb190af53bdeeefb35303",
   "md5":"e04caf8af57019c64e1ae39b9d196502",
   "func_name":"samba-4_@_9_@_5+dfsg-5/source3/winbindd/winbindd_util_@_c/winbindd_dual_init_connection/777",
   "func":"enum winbindd_result winbindd_dual_init_connection(struct winbindd_domain *@@var_1@@domain@@,\n\t\t\t\t\t\t   struct winbindd_cli_state *@@var_3@@state@@)\n{\n\t\n\t@@var_3@@state@@->request->domain_name\n\t\t[sizeof(@@var_3@@state@@->request->domain_name)-1]='\\0';\n\t@@var_3@@state@@->request->data.init_conn.dcname\n\t\t[sizeof(@@var_3@@state@@->request->data.init_conn.dcname)-1]='\\0';\n\n\tif (strlen(@@var_3@@state@@->request->data.init_conn.dcname) > 0) {\n\t\tTALLOC_FREE(@@var_1@@domain@@->dcname);\n\t\t@@var_1@@domain@@->dcname = talloc_strdup(@@var_1@@domain@@,\n\t\t\t\t@@var_3@@state@@->request->data.init_conn.dcname);\n\t\tif (@@var_1@@domain@@->dcname == NULL) {\n\t\t\treturn @@var_4@@WINBINDD_ERROR@@;\n\t\t}\n\t}\n\n\tinit_dc_connection(@@var_1@@domain@@, (0));\n\n\tif (!@@var_1@@domain@@->initialized) {\n\t\t\n\t\tDEBUG(5, (\"winbindd_dual_init_connection: %s returning without initialization \"\n\t\t\t\"online = %d\\n\", @@var_1@@domain@@->name, (int)@@var_1@@domain@@->online ));\n\t}\n\n\tfstrcpy(@@var_3@@state@@->response->data.domain_info.name, @@var_1@@domain@@->name);\n\tfstrcpy(@@var_3@@state@@->response->data.domain_info.alt_name, @@var_1@@domain@@->alt_name);\n\tsid_to_fstring(@@var_3@@state@@->response->data.domain_info.sid, &@@var_1@@domain@@->sid);\n\n\t@@var_3@@state@@->response->data.domain_info.native_mode\n\t\t= @@var_1@@domain@@->native_mode;\n\t@@var_3@@state@@->response->data.domain_info.active_directory\n\t\t= @@var_1@@domain@@->active_directory;\n\t@@var_3@@state@@->response->data.domain_info.primary\n\t\t= @@var_1@@domain@@->primary;\n\n\treturn @@var_2@@WINBINDD_OK@@;\n}",
   "norm_func":"enum winbindd_result winbindd_dual_init_connection(struct winbindd_domain *@@var_1@@domain@@,\n\t\t\t\t\t\t   struct winbindd_cli_state *@@var_3@@state@@)\n{\n\t\n\t@@var_3@@state@@->request->domain_name\n\t\t[sizeof(@@var_3@@state@@->request->domain_name)-1]='\\0';\n\t@@var_3@@state@@->request->data.init_conn.dcname\n\t\t[sizeof(@@var_3@@state@@->request->data.init_conn.dcname)-1]='\\0';\n\n\tif (strlen(@@var_3@@state@@->request->data.init_conn.dcname) > 0) {\n\t\tTALLOC_FREE(@@var_1@@domain@@->dcname);\n\t\t@@var_1@@domain@@->dcname = talloc_strdup(@@var_1@@domain@@,\n\t\t\t\t@@var_3@@state@@->request->data.init_conn.dcname);\n\t\tif (@@var_1@@domain@@->dcname == NULL) {\n\t\t\treturn @@var_4@@winbindd_error@@;\n\t\t}\n\t}\n\n\tinit_dc_connection(@@var_1@@domain@@, (0));\n\n\tif (!@@var_1@@domain@@->initialized) {\n\t\t\n\t\tDEBUG(5, (\"winbindd_dual_init_connection: %s returning without initialization \"\n\t\t\t\"online = %d\\n\", @@var_1@@domain@@->name, (int)@@var_1@@domain@@->online ));\n\t}\n\n\tfstrcpy(@@var_3@@state@@->response->data.domain_info.name, @@var_1@@domain@@->name);\n\tfstrcpy(@@var_3@@state@@->response->data.domain_info.alt_name, @@var_1@@domain@@->alt_name);\n\tsid_to_fstring(@@var_3@@state@@->response->data.domain_info.sid, &@@var_1@@domain@@->sid);\n\n\t@@var_3@@state@@->response->data.domain_info.native_mode\n\t\t= @@var_1@@domain@@->native_mode;\n\t@@var_3@@state@@->response->data.domain_info.active_directory\n\t\t= @@var_1@@domain@@->active_directory;\n\t@@var_3@@state@@->response->data.domain_info.primary\n\t\t= @@var_1@@domain@@->primary;\n\n\treturn @@var_2@@winbindd_ok@@;\n}",
   "var":[
      "domain",
      "WINBINDD_OK",
      "state",
      "WINBINDD_ERROR"
   ],
   "vars_map":[
      [
         "domain",
         "domain"
      ],
      [
         "WINBINDD_OK",
         "winbindd_ok"
      ],
      [
         "state",
         "state"
      ],
      [
         "WINBINDD_ERROR",
         "winbindd_error"
      ]
   ]
}
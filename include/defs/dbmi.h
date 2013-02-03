#ifndef GRASS_DBMIDEFS_H
#define GRASS_DBMIDEFS_H

void db_Cstring_to_lowercase(char *);
void db_Cstring_to_uppercase(char *);
int db_add_column(dbDriver *, dbString *, dbColumn *);
void db__add_cursor_to_driver_state(dbCursor *);
int db_alloc_cursor_column_flags(dbCursor *);
int db_alloc_cursor_table(dbCursor *, int);
int db_append_table_column(dbTable * , dbColumn *);
dbDirent *db_alloc_dirent_array(int);
dbHandle *db_alloc_handle_array(int);
dbIndex *db_alloc_index_array(int);
int db_alloc_index_columns(dbIndex *, int);
dbString *db_alloc_string_array(int);
dbTable *db_alloc_table(int);
int db_append_string(dbString *, const char *);
void db_auto_print_errors(int);
void db_auto_print_protocol_errors(int);
int db_bind_update(dbCursor *);
void *db_calloc(int, int);
int db_CatValArray_alloc(dbCatValArray *, int);
int db_CatValArray_realloc(dbCatValArray *, int);
void db_CatValArray_free(dbCatValArray *);
void db_CatValArray_init(dbCatValArray *);
void db_CatValArray_sort(dbCatValArray *);
int db_CatValArray_sort_by_value(dbCatValArray *);
int db_CatValArray_get_value(dbCatValArray *, int, dbCatVal **);
int db_CatValArray_get_value_int(dbCatValArray *, int, int *);
int db_CatValArray_get_value_double(dbCatValArray *, int,
				    double *);
void db_char_to_lowercase(char *);
void db_char_to_uppercase(char *);
void db_clear_error(void);
dbTable *db_clone_table(dbTable *);
void db__close_all_cursors(void);
int db_close_cursor(dbCursor *);
int db_close_database(dbDriver *);
int db_close_database_shutdown_driver(dbDriver *);
int db_column_sqltype(dbDriver *, const char *, const char *);
int db_column_Ctype(dbDriver *, const char *, const char *);
int db_convert_Cstring_to_column_default_value(const char *,
					       dbColumn *);
int db_convert_Cstring_to_column_value(const char *,
				       dbColumn *);
int db_convert_Cstring_to_value(const char *, int,
				dbValue *);
int db_convert_Cstring_to_value_datetime(const char *, int,
					 dbValue *);
int db_convert_column_default_value_to_string(dbColumn *,
					      dbString *);
int db_convert_column_value_to_string(dbColumn *, dbString *);
int db_convert_value_datetime_into_string(dbValue *, int,
					  dbString *);
int db_convert_value_to_string(dbValue *, int,
			       dbString *);
dbColumn *db_copy_column(dbColumn *, dbColumn *);
void db_copy_dbmscap_entry(dbDbmscap *, dbDbmscap *);
int db_copy_string(dbString *, const dbString *);
int db_table_to_sql(dbTable *, dbString *);
int db_copy_table(const char *, const char *, const char *, const char *,
		  const char *, const char *);
int db_copy_table_where(const char *, const char *, const char *,
			const char *, const char *, const char *,
			const char *);
int db_copy_table_select(const char *, const char *, const char *,
			 const char *, const char *, const char *,
			 const char *);
int db_copy_table_by_ints(const char *, const char *, const char *,
			  const char *, const char *, const char *,
			  const char *, int *, int);
void db_copy_value(dbValue *, dbValue *);
int db_create_database(dbDriver *, dbHandle *);
int db_create_index(dbDriver *, dbIndex *);
int db_create_index2(dbDriver *, const char *,
		     const char *);
int db_create_table(dbDriver *, dbTable *);
int db_d_add_column(void);
int db_d_bind_update(void);
const char *db_dbmscap_filename(void);
int db_d_close_cursor(void);
int db_d_close_database(void);
int db_d_create_database(void);
int db_d_create_index(void);
int db_d_create_table(void);
int db_d_delete(void);
int db_d_delete_database(void);
int db_d_describe_table(void);
int db_d_drop_column(void);
int db_d_drop_index(void);
int db_d_drop_table(void);
void db_debug(const char *);
void db_debug_off(void);
void db_debug_on(void);
int db_delete(dbCursor *);
int db_delete_database(dbDriver *, dbHandle *);
int db_delete_table(const char *, const char *, const char *);
int db_describe_table(dbDriver *, dbString *, dbTable **);
int db_d_execute_immediate(void);
int db_d_begin_transaction(void);
int db_d_commit_transaction(void);
int db_d_fetch(void);
int db_d_find_database(void);
int db_d_get_num_rows(void);
int db_d_grant_on_table(void);
int db_d_insert(void);
void db_d_init_error(const char *);
void db_d_append_error(const char *, ...)
    __attribute__ ((format(printf, 1, 2)));
void db_d_report_error(void);
dbDirent *db_dirent(const char *, int *);
int db_d_list_databases(void);
int db_d_list_indexes(void);
int db_d_list_tables(void);
int db_d_open_database(void);
int db_d_open_insert_cursor(void);
int db_d_open_select_cursor(void);
int db_d_open_update_cursor(void);
void db_double_quote_string(dbString *);
int db_driver(int, char **);

int db_driver_mkdir(const char *, int, int);
int db_drop_column(dbDriver *, dbString *,
		   dbString *);
void db__drop_cursor_from_driver_state(dbCursor *);
int db_drop_index(dbDriver *, dbString *);
int db_drop_table(dbDriver *, dbString *);
void db_drop_token(dbToken);
int db_d_update(void);
int db_d_version(void);
int db_enlarge_string(dbString *, int);
void db_error(const char *);
int db_execute_immediate(dbDriver *, dbString *);
int db_begin_transaction(dbDriver *);
int db_commit_transaction(dbDriver *);
int db_fetch(dbCursor *, int, int *);
int db_find_database(dbDriver *, dbHandle *, int *);
dbAddress db_find_token(dbToken);
void db_free(void *);
void db_free_column(dbColumn *);
void db_free_cursor(dbCursor *);
void db_free_cursor_column_flags(dbCursor *);
void db_free_dbmscap(dbDbmscap *);
void db_free_dirent_array(dbDirent *, int);
void db_free_handle(dbHandle *);
void db_free_handle_array(dbHandle *, int);
void db_free_index(dbIndex *);
void db_free_index_array(dbIndex *, int);
void db_free_string(dbString *);
void db_free_string_array(dbString *, int);
void db_free_table(dbTable *);
int db_get_column(dbDriver *, const char *, const char *,
		  dbColumn **);
dbValue *db_get_column_default_value(dbColumn *);
const char *db_get_column_description(dbColumn *);
int db_get_column_host_type(dbColumn *);
int db_get_column_length(dbColumn *);
const char *db_get_column_name(dbColumn *);
int db_get_column_precision(dbColumn *);
int db_get_column_scale(dbColumn *);
int db_get_column_select_priv(dbColumn *);
int db_get_column_sqltype(dbColumn *);
int db_get_column_update_priv(dbColumn *);
dbValue *db_get_column_value(dbColumn *);
int db_get_connection(dbConnection *);
int db_get_cursor_number_of_columns(dbCursor *);
dbTable *db_get_cursor_table(dbCursor *);
dbToken db_get_cursor_token(dbCursor *);
const char *db_get_default_driver_name(void);
const char *db_get_default_database_name(void);
const char *db_get_default_schema_name(void);
const char *db_get_default_group_name(void);
dbDriverState *db__get_driver_state(void);
int db_get_error_code(void);
const char *db_get_error_msg(void);
const char *db_get_error_who(void);
const char *db_get_handle_dbname(dbHandle *);
const char *db_get_handle_dbschema(dbHandle *);
const char *db_get_index_column_name(dbIndex *, int);
const char *db_get_index_name(dbIndex *);
int db_get_index_number_of_columns(dbIndex *);
const char *db_get_index_table_name(dbIndex *);
int db_get_num_rows(dbCursor *);
char *db_get_string(const dbString *);
dbColumn *db_get_table_column(dbTable *, int);
dbColumn *db_get_table_column_by_name(dbTable *, const char*);
int db_get_table_delete_priv(dbTable *);
const char *db_get_table_description(dbTable *);
int db_get_table_insert_priv(dbTable *);
const char *db_get_table_name(dbTable *);
int db_get_table_number_of_columns(dbTable *);
int db_get_table_number_of_rows(dbDriver *, dbString *);
int db_get_table_select_priv(dbTable *);
int db_get_table_update_priv(dbTable *);
double db_get_value_as_double(dbValue *, int);
int db_get_value_day(dbValue *);
double db_get_value_double(dbValue *);
int db_get_value_hour(dbValue *);
int db_get_value_int(dbValue *);
int db_get_value_minute(dbValue *);
int db_get_value_month(dbValue *);
double db_get_value_seconds(dbValue *);
const char *db_get_value_string(dbValue *);
int db_get_value_year(dbValue *);
int db_grant_on_table(dbDriver *, const char *, int,
		      int);
int db_has_dbms(void);
void db_init_column(dbColumn *);
void db_init_cursor(dbCursor *);
void db__init_driver_state(void);
void db_init_handle(dbHandle *);
void db_init_index(dbIndex *);
void db_init_string(dbString *);
void db_init_table(dbTable *);
int db_insert(dbCursor *);
void db_interval_range(int, int *, int *);
int db_isdir(const char *);
int db_legal_tablename(const char *);
int db_list_databases(dbDriver *, dbString *, int,
		      dbHandle **, int *);
const char *db_list_drivers(void);
int db_list_indexes(dbDriver *, dbString *, dbIndex **,
		    int *);
int db_list_tables(dbDriver *, dbString **, int *,
		   int);
void *db_malloc(int);
void db__mark_database_closed(void);
void db__mark_database_open(const char *, const char *);
void db_memory_error(void);
dbToken db_new_token(dbAddress);
int db_nocase_compare(const char *, const char *);
void db_noproc_error(int);
int db_open_database(dbDriver *, dbHandle *);
int db_open_insert_cursor(dbDriver *, dbCursor *);
int db_open_select_cursor(dbDriver *, dbString *,
			  dbCursor *, int);
int db_open_update_cursor(dbDriver *, dbString *_name,
			  dbString *, dbCursor *, int);
void db_print_column_definition(FILE *, dbColumn *);
void db_print_error(void);
void db_print_index(FILE *, dbIndex *);
void db_print_table_definition(FILE *, dbTable *);
void db_procedure_not_implemented(const char *);
void db_protocol_error(void);
dbDbmscap *db_read_dbmscap(void);
void *db_realloc(void *, int);
int db__recv_char(char *);
int db__recv_column_default_value(dbColumn *);
int db__recv_column_definition(dbColumn *);
int db__recv_column_value(dbColumn *);
int db__recv_datetime(dbDateTime *);
int db__recv_double(double *);
int db__recv_double_array(double **, int *);
int db__recv_float(float *);
int db__recv_float_array(float **, int *);
int db__recv_handle(dbHandle *);
int db__recv_index(dbIndex *);
int db__recv_index_array(dbIndex **, int *);
int db__recv_int(int *);
int db__recv_int_array(int **, int *);
int db__recv_procnum(int *);
int db__recv_return_code(int *);
int db__recv_short(short *);
int db__recv_short_array(short **, int *);
int db__recv_string(dbString *);
int db__recv_string_array(dbString **, int *);
int db__recv_table_data(dbTable *);
int db__recv_table_definition(dbTable **);
int db__recv_token(dbToken *);
int db__recv_value(dbValue *, int);
int db__send_Cstring(const char *);
int db__send_char(int);
int db__send_column_default_value(dbColumn *);
int db__send_column_definition(dbColumn *);
int db__send_column_value(dbColumn *);
int db__send_datetime(dbDateTime *);
int db__send_double(double);
int db__send_double_array(const double *, int);
int db__send_failure(void);
int db__send_float(float);
int db__send_float_array(const float *, int);
int db__send_handle(dbHandle *);
int db__send_index(dbIndex *);
int db__send_index_array(dbIndex *, int);
int db__send_int(int);
int db__send_int_array(const int *, int);
int db__send_procedure_not_implemented(int);
int db__send_procedure_ok(int);
int db__send_short(int);
int db__send_short_array(const short *, int);
int db__send_string(dbString *);
int db__send_string_array(dbString *, int);
int db__send_success(void);
int db__send_table_data(dbTable *);
int db__send_table_definition(dbTable *);
int db__send_token(dbToken *);
int db__send_value(dbValue *, int);
int db_select_CatValArray(dbDriver *, const char *, const char *,
			  const char *, const char *,
			  dbCatValArray *);
int db_select_int(dbDriver *, const char *, const char *,
		  const char *, int **);
int db_select_value(dbDriver *, const char *, const char *,
		    int, const char *, dbValue *);
int db_set_column_description(dbColumn *, const char *);
void db_set_column_has_defined_default_value(dbColumn *);
void db_set_column_has_undefined_default_value(dbColumn *);
void db_set_column_host_type(dbColumn *, int);
void db_set_column_length(dbColumn *, int);
int db_set_column_name(dbColumn *, const char *);
void db_set_column_null_allowed(dbColumn *);
void db_set_column_precision(dbColumn *, int);
void db_set_column_scale(dbColumn *, int);
void db_set_column_select_priv_granted(dbColumn *);
void db_set_column_select_priv_not_granted(dbColumn *);
void db_set_column_sqltype(dbColumn *, int);
void db_set_column_update_priv_granted(dbColumn *);
void db_set_column_update_priv_not_granted(dbColumn *);
void db_set_column_use_default_value(dbColumn *);
int db_set_connection(dbConnection *);
void db_set_cursor_column_flag(dbCursor *, int);
void db_set_cursor_column_for_update(dbCursor *, int);
void db_set_cursor_mode(dbCursor *, int);
void db_set_cursor_mode_insensitive(dbCursor *);
void db_set_cursor_mode_scroll(dbCursor *);
void db_set_cursor_table(dbCursor *, dbTable *);
void db_set_cursor_token(dbCursor *, dbToken);
void db_set_cursor_type_insert(dbCursor *);
void db_set_cursor_type_readonly(dbCursor *);
void db_set_cursor_type_update(dbCursor *);
int db_set_default_connection(void);
void db_set_error_who(const char *);
int db_set_handle(dbHandle *, const char *, const char *);
int db_set_index_column_name(dbIndex *, int,
			     const char *);
int db_set_index_name(dbIndex *, const char *);
int db_set_index_table_name(dbIndex *, const char *);
int db_set_index_type_non_unique(dbIndex *);
int db_set_index_type_unique(dbIndex *);
void db__set_protocol_fds(FILE *, FILE *);
int db_set_string(dbString *, const char *);
int db_set_string_no_copy(dbString *, char *);
int db_set_table_column(dbTable *, int, dbColumn *);
void db_set_table_delete_priv_granted(dbTable *);
void db_set_table_delete_priv_not_granted(dbTable *);
int db_set_table_description(dbTable *, const char *);
void db_set_table_insert_priv_granted(dbTable *);
void db_set_table_insert_priv_not_granted(dbTable *);
int db_set_table_name(dbTable *, const char *);
void db_set_table_select_priv_granted(dbTable *);
void db_set_table_select_priv_not_granted(dbTable *);
void db_set_table_update_priv_granted(dbTable *);
void db_set_table_update_priv_not_granted(dbTable *);
void db_set_value_datetime_current(dbValue *);
void db_set_value_datetime_not_current(dbValue *);
void db_set_value_day(dbValue *, int);
void db_set_value_double(dbValue *, double);
void db_set_value_hour(dbValue *, int);
void db_set_value_int(dbValue *, int);
void db_set_value_minute(dbValue *, int);
void db_set_value_month(dbValue *, int);
void db_set_value_not_null(dbValue *);
void db_set_value_null(dbValue *);
void db_set_value_seconds(dbValue *, double);
int db_set_value_string(dbValue *, const char *);
void db_set_value_year(dbValue *, int);
int db_shutdown_driver(dbDriver *);
const char *db_sqltype_name(int);
int db_sqltype_to_Ctype(int);
dbDriver *db_start_driver(const char *);
dbDriver *db_start_driver_open_database(const char *, const char *);
int db__start_procedure_call(int);
char *db_store(const char *);
void db_strip(char *);
void db_syserror(const char *);
int db_table_exists(const char *, const char *,
		    const char *);
int db_test_column_has_default_value(dbColumn *);
int db_test_column_has_defined_default_value(dbColumn *);
int db_test_column_has_undefined_default_value(dbColumn *);
int db_test_column_null_allowed(dbColumn *);
int db_test_column_use_default_value(dbColumn *);
int db_test_cursor_any_column_flag(dbCursor *);
int db_test_cursor_any_column_for_update(dbCursor *);
int db_test_cursor_column_flag(dbCursor *, int);
int db_test_cursor_column_for_update(dbCursor *, int);
int db_test_cursor_mode_insensitive(dbCursor *);
int db_test_cursor_mode_scroll(dbCursor *);
int db_test_cursor_type_fetch(dbCursor *);
int db_test_cursor_type_insert(dbCursor *);
int db_test_cursor_type_update(dbCursor *);
int db__test_database_open(void);
int db_test_index_type_unique(dbIndex *);
int db_test_value_datetime_current(dbValue *);
int db_test_value_isnull(dbValue *);
void db_unset_column_has_default_value(dbColumn *);
void db_unset_column_null_allowed(dbColumn *);
void db_unset_column_use_default_value(dbColumn *);
void db_unset_cursor_column_flag(dbCursor *, int);
void db_unset_cursor_column_for_update(dbCursor *, int);
void db_unset_cursor_mode(dbCursor *);
void db_unset_cursor_mode_insensitive(dbCursor *);
void db_unset_cursor_mode_scroll(dbCursor *);
int db_update(dbCursor *);
int db_gversion(dbDriver *, dbString *,
		dbString *);
const char *db_whoami(void);
void db_zero(void *, int);
void db_zero_string(dbString *);
unsigned int db_sizeof_string(const dbString *);
int db_set_login(const char *, const char *, const char *, const char *);
int db_get_login(const char *, const char *, const char **, const char **);

#endif

def edit_column_names(df):
    """
    Edits the column names of the DataFrame to make them consistent and in English.

    Parameters:
    - df (pd.DataFrame): The DataFrame whose columns need to be renamed.

    Returns:
    - pd.DataFrame: The DataFrame with updated column names.
    """
    # Drop unnamed columns
    df.drop(columns=[col for col in df.columns if 'Unnamed' in col], inplace=True)

    # Rename columns to English
    df.rename(columns={
        'ID': 'id',
        'Timestamp': 'timestamp',
        'תאריך': 'date',
        'חודש': 'month',
        'חציון': 'half_year',
        'חציון number': 'half_year_number',
        'month number': 'month_number',
        'שעה מדויק': 'exact_hour',
        'שעה עגולה': 'rounded_hour',
        'מיקום': 'location',
        'אבני ק״מ': 'km_stones',
        'כיוון': 'direction',
        'מספר מנהרה או מחלף': 'tunnel_or_interchange_number',
        'נ.צ.': 'coordinates',
        'סוג תאונה': 'accident_type',
        'סוג רכב א (המסתמן כאשם)': 'vehicle_type_a',
        'סוג רכב ב\'': 'vehicle_type_b',
        'סוג רכב ג': 'vehicle_type_c',
        'סוג רכב ד\'': 'vehicle_type_d',
        'סוג רכב ה\'': 'vehicle_type_e',
        'חומרת תאונה': 'accident_severity',
        'הרוגים': 'fatalities',
        'פצועים קשה': 'serious_injuries',
        'פצועים קל': 'minor_injuries',
        'סהכ נפגעים': 'total_injuries',
        'מהירות נסיעה (בכיוון נסיעת רכב א)': 'travel_speed',
        'מצב מיסעה': 'road_condition',
        'סוג דרך': 'road_type',
        'מזג אויר': 'weather',
        'מצב תאורה': 'lighting_condition',
        'מצב תאורה + חומרת תאונה': 'lighting_condition_accident_severity',
        'סוג תאונה + חומרת תאונה': 'accident_type_severity',
        'סוג תאונה + חומרת תאונה + סהכ נפגעים': 'accident_type_severity_total_injuries',
        'מס אירווע בגיב ': 'event_number'
    }, inplace=True)

    return df

## OCR接口文档

### 1. 获取文件列表

#### 调用地址

ocr/recognize/files

#### 参数

|字段|必选|类型|说明|
|----|----|----|----|
|table_name|true|string|存json->文件夹名称 存数据库->表名称|

#### 返回

|返回值字段|字段类型|字段说明|
|----------|--------|--------|
|status_code|int|状态码|
|message|string|状态描述信息|
|file_list|array|文件列表信息|

##### 返回字段 "file_list" 子项

|返回值字段|字段类型|字段说明|
|----------|--------|--------|
|file_name|string|文件名|
|file_id|string|文件id|


### 2. 获取文件识别结果

#### 调用地址

ocr/recognize/results

#### 参数

|字段|必选|类型|说明|
|----|----|----|----|
|file_id|true|string|文件id|

#### 返回

|返回值字段|字段类型|字段说明|
|----------|--------|--------|
|status_code|int|状态码|
|message|string|状态描述信息|
|file_name|string|文件名|
|file_id|string|文件id|
|is_modified|bool|是否已修改|
|update_time|string|最后更新的时间|
|results|array|每一页检测和识别的结果|

##### 返回字段 "results" 子项

|返回值字段|字段类型|字段说明|
|----------|--------|--------|
|image_name|string|图片文件名|
|image_base64|string|图片base64编码|
|page_resluts|array|页面元素的识别结果|

##### 返回字段 "page_results" 子项

|返回值字段|字段类型|字段说明|
|----------|--------|--------|
|element_type|string|页面元素类型table或者text|
|location|array[8]|页面元素的坐标|
|content|string|页面元素的识别结果|
|probability|array|识别结果对应字符的概率|

##### element_type = table 返回字段 "results" 子项

|返回值字段|字段类型|字段说明|
|----------|--------|--------|
|cell_location|array[4]|单元格的起始坐标|
|cell_content|string|单元格的识别结果|
|cell_probability|array|识别结果对应字符的概率|

### 3. 提交修正结果

#### 调用地址

ocr/recognize/submit

#### 参数

|字段|必选|类型|说明|
|----|----|----|----|
|file_name|true|string|文件名|
|file_id|true|string|文件id|
|is_modified|true|bool|是否已修改|
|results|true|array|每一页检测和识别的结果|

##### 请求字段 "results" 子项

|返回值字段|字段类型|字段说明|
|----------|--------|--------|
|image_name|string|图片文件名|
|image_base64|string|图片base64编码|
|page_resluts|array|页面元素的识别结果|

##### 请求字段 "page_results" 子项

|返回值字段|字段类型|字段说明|
|----------|--------|--------|
|element_type|string|页面元素类型table或者text|
|location|array[8]|页面元素的坐标|
|content|string|页面元素的识别结果|
|probability|array|识别结果对应字符的概率|

##### element_type = table 请求字段 "results" 子项

|返回值字段|字段类型|字段说明|
|----------|--------|--------|
|cell_location|array[4]|单元格的起始坐标|
|cell_content|string|单元格的识别结果|
|cell_probability|array|识别结果对应字符的概率|

#### 返回

|返回值字段|字段类型|字段说明|
|----------|--------|--------|
|status_code|int|状态码|
|message|string|状态描述信息|

### 4. 获取文件列表

#### 调用地址

ocr/recognize/export

#### 参数

|字段|必选|类型|说明|
|----|----|----|----|
|export_type|true|string|txt、html、docx->example.zip|

#### 返回

|返回值字段|字段类型|字段说明|
|----------|--------|--------|
|status_code|int|状态码|
|message|string|状态描述信息|
|file_list|array|文件列表信息|

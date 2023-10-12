#!/usr/bin/env python3.8
import sublime
import sublime_plugin
import os
import subprocess

class VerilogFormatterCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    # 获取当前打开文件的文件路径
    file_path = self.view.file_name()
    
    if file_path:
      # 检查文件后缀是否为 .v
      if file_path.endswith(".v"):

        # 获取当前文件内容
        current_content = self.view.substr(sublime.Region(0, self.view.size()))

        # 在这里定义你要执行的Windows命令
        command = (
          "D:\\Downloads\\verible-v0.0-3418-ge76eb275-win64\\verible-verilog-format.exe "
          "--column_limit=300 "
          "--wrap_spaces=2 "
          "--indentation_spaces=2 "
          "--assignment_statement_alignment=align "
          "--named_port_alignment=align "
          "--port_declarations_alignment=align "
          "--module_net_variable_alignment=align "
          "--case_items_alignment=align "
          "--distribution_items_alignment=align "
          "--enum_assignment_statement_alignment=align "
          "--formal_parameters_alignment=align "
          "--named_parameter_alignment=align "
          "--try_wrap_long_lines=true "
          "--wrap_end_else_clauses=true "
          "--failsafe_success=false "
          f'"{file_path}"'
        )
        
        try:
          # 使用subprocess模块执行Windows命令
          result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, encoding='cp1252')
          
          # 比较当前文件内容和命令输出
          if current_content != result:
            # 清空当前文件
            self.view.erase(edit, sublime.Region(0, self.view.size()))

            # 在当前文件中插入命令输出
            self.view.insert(edit, 0, result)
          else:
            sublime.status_message("File content has not changed.")

        except subprocess.CalledProcessError as e:
          # 如果命令执行出错，可以在控制台中输出错误信息
          print("Error: ", e.output)
      else:
        sublime.status_message("Current file is not a Verilog file.")
    else:
      # 使用message_dialog()显示文件未打开的提示
      sublime.status_message("No file is currently open.")

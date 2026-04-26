#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
订单数据 ETL 脚本
功能：
1. 从 CSV 文件读取用户订单数据
2. 清洗并转换日期格式
3. 去重处理
4. 写入 PostgreSQL 数据库
5. 输出处理摘要报告
"""

import os
import sys
import logging
from datetime import datetime
from typing import Dict, Any, Optional

import pandas as pd
from dateutil.parser import parse
from sqlalchemy import create_engine, text, Table, MetaData, Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(f'etl_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)


class OrderETL:
    """订单数据 ETL 处理器"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化 ETL 处理器
        
        Args:
            config: 配置字典，包含数据库连接信息等
        """
        self.config = config or {}
        self.stats = {
            'start_time': None,
            'end_time': None,
            'total_rows_read': 0,
            'rows_after_cleaning': 0,
            'duplicates_removed': 0,
            'rows_written_to_db': 0,
            'errors': []
        }
        self.engine = None
        self.df = None
        
    def load_config_from_env(self):
        """从环境变量或 .env 文件加载配置"""
        load_dotenv()
        
        self.config['db'] = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME', 'orders_db'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', ''),
            'table': os.getenv('DB_TABLE', 'orders')
        }
        
        logger.info("配置已从环境变量加载")
        
    def connect_to_database(self):
        """连接到 PostgreSQL 数据库"""
        try:
            db_config = self.config.get('db', {})
            connection_string = (
                f"postgresql+psycopg2://{db_config.get('user')}:"
                f"{db_config.get('password')}@{db_config.get('host')}:"
                f"{db_config.get('port')}/{db_config.get('database')}"
            )
            
            self.engine = create_engine(connection_string)
            
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                conn.commit()
            
            logger.info("成功连接到 PostgreSQL 数据库")
            return True
            
        except SQLAlchemyError as e:
            error_msg = f"数据库连接失败: {str(e)}"
            logger.error(error_msg)
            self.stats['errors'].append(error_msg)
            return False
            
    def create_table_if_not_exists(self):
        """创建订单表（如果不存在）"""
        try:
            metadata = MetaData()
            
            orders_table = Table(
                self.config['db']['table'],
                metadata,
                Column('order_id', String(50), primary_key=True, comment='订单ID'),
                Column('user_id', String(50), nullable=False, comment='用户ID'),
                Column('order_date', DateTime, nullable=False, comment='订单日期'),
                Column('amount', Float, nullable=False, comment='订单金额'),
                Column('status', String(20), nullable=False, comment='订单状态'),
                Column('product_name', String(200), comment='产品名称'),
                Column('quantity', Integer, comment='数量'),
                Column('created_at', DateTime, default=datetime.now, comment='记录创建时间'),
                Column('updated_at', DateTime, default=datetime.now, onupdate=datetime.now, comment='记录更新时间'),
                extend_existing=True
            )
            
            metadata.create_all(self.engine)
            logger.info(f"表 '{self.config['db']['table']}' 已创建或已存在")
            return True
            
        except SQLAlchemyError as e:
            error_msg = f"创建表失败: {str(e)}"
            logger.error(error_msg)
            self.stats['errors'].append(error_msg)
            return False
            
    def parse_date(self, date_str: Any) -> Optional[datetime]:
        """
        智能解析日期格式
        
        Args:
            date_str: 日期字符串或其他类型
            
        Returns:
            解析后的 datetime 对象，解析失败返回 None
        """
        if pd.isna(date_str) or date_str == '':
            return None
            
        if isinstance(date_str, datetime):
            return date_str
            
        if isinstance(date_str, pd.Timestamp):
            return date_str.to_pydatetime()
            
        try:
            date_str = str(date_str).strip()
            
            formats_to_try = [
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d %H:%M',
                '%Y-%m-%d',
                '%Y/%m/%d %H:%M:%S',
                '%Y/%m/%d %H:%M',
                '%Y/%m/%d',
                '%d-%m-%Y %H:%M:%S',
                '%d-%m-%Y',
                '%d/%m/%Y %H:%M:%S',
                '%d/%m/%Y',
                '%m/%d/%Y %H:%M:%S',
                '%m/%d/%Y',
                '%Y年%m月%d日 %H:%M:%S',
                '%Y年%m月%d日',
            ]
            
            for fmt in formats_to_try:
                try:
                    return datetime.strptime(date_str, fmt)
                except (ValueError, TypeError):
                    continue
                    
            parsed = parse(date_str, fuzzy=True)
            return parsed
            
        except (ValueError, TypeError, Exception) as e:
            logger.warning(f"无法解析日期: {date_str}, 错误: {str(e)}")
            return None
            
    def read_csv(self, csv_path: str) -> bool:
        """
        从 CSV 文件读取数据
        
        Args:
            csv_path: CSV 文件路径
            
        Returns:
            读取成功返回 True，否则返回 False
        """
        try:
            if not os.path.exists(csv_path):
                error_msg = f"CSV 文件不存在: {csv_path}"
                logger.error(error_msg)
                self.stats['errors'].append(error_msg)
                return False
                
            logger.info(f"开始读取 CSV 文件: {csv_path}")
            
            self.df = pd.read_csv(
                csv_path,
                encoding='utf-8',
                dtype={
                    'order_id': str,
                    'user_id': str,
                    'product_name': str,
                    'status': str
                },
                low_memory=False
            )
            
            self.stats['total_rows_read'] = len(self.df)
            logger.info(f"成功读取 {self.stats['total_rows_read']} 条记录")
            
            return True
            
        except Exception as e:
            error_msg = f"读取 CSV 文件失败: {str(e)}"
            logger.error(error_msg)
            self.stats['errors'].append(error_msg)
            return False
            
    def clean_and_transform(self) -> bool:
        """
        清洗和转换数据
        
        Returns:
            处理成功返回 True，否则返回 False
        """
        try:
            if self.df is None or self.df.empty:
                error_msg = "没有数据可供清洗"
                logger.error(error_msg)
                self.stats['errors'].append(error_msg)
                return False
                
            logger.info("开始数据清洗和转换")
            
            required_columns = ['order_id', 'user_id', 'order_date', 'amount', 'status']
            missing_columns = [col for col in required_columns if col not in self.df.columns]
            
            if missing_columns:
                error_msg = f"缺少必要的列: {', '.join(missing_columns)}"
                logger.error(error_msg)
                self.stats['errors'].append(error_msg)
                return False
                
            self.df.columns = self.df.columns.str.strip().str.lower()
            
            self.df['order_id'] = self.df['order_id'].astype(str).str.strip()
            self.df['user_id'] = self.df['user_id'].astype(str).str.strip()
            
            initial_count = len(self.df)
            self.df = self.df.dropna(subset=['order_id', 'order_date', 'amount'])
            self.df = self.df[self.df['order_id'] != '']
            dropped_count = initial_count - len(self.df)
            if dropped_count > 0:
                logger.info(f"删除了 {dropped_count} 条包含缺失关键字段的记录")
            
            logger.info("转换日期格式")
            self.df['order_date'] = self.df['order_date'].apply(self.parse_date)
            
            invalid_dates = self.df['order_date'].isna().sum()
            if invalid_dates > 0:
                logger.warning(f"发现 {invalid_dates} 条无效日期记录，将被删除")
                self.df = self.df.dropna(subset=['order_date'])
                
            logger.info("转换金额格式")
            self.df['amount'] = pd.to_numeric(self.df['amount'], errors='coerce')
            invalid_amounts = self.df['amount'].isna().sum()
            if invalid_amounts > 0:
                logger.warning(f"发现 {invalid_amounts} 条无效金额记录，将被删除")
                self.df = self.df.dropna(subset=['amount'])
            
            self.df['status'] = self.df['status'].astype(str).str.strip().str.lower()
            
            valid_statuses = ['pending', 'completed', 'cancelled', 'refunded', 'shipped', 
                              '待处理', '已完成', '已取消', '已退款', '已发货']
            self.df.loc[~self.df['status'].isin(valid_statuses), 'status'] = 'unknown'
            
            if 'quantity' in self.df.columns:
                self.df['quantity'] = pd.to_numeric(self.df['quantity'], errors='coerce').fillna(1).astype(int)
            
            if 'product_name' in self.df.columns:
                self.df['product_name'] = self.df['product_name'].astype(str).str.strip()
            
            self.stats['rows_after_cleaning'] = len(self.df)
            logger.info(f"数据清洗完成，剩余 {self.stats['rows_after_cleaning']} 条有效记录")
            
            return True
            
        except Exception as e:
            error_msg = f"数据清洗失败: {str(e)}"
            logger.error(error_msg)
            self.stats['errors'].append(error_msg)
            return False
            
    def remove_duplicates(self) -> bool:
        """
        去重处理
        
        Returns:
            处理成功返回 True，否则返回 False
        """
        try:
            if self.df is None or self.df.empty:
                error_msg = "没有数据可供去重"
                logger.error(error_msg)
                self.stats['errors'].append(error_msg)
                return False
                
            logger.info("开始去重处理")
            
            before_count = len(self.df)
            
            self.df = self.df.drop_duplicates(subset=['order_id'], keep='first')
            
            self.stats['duplicates_removed'] = before_count - len(self.df)
            
            logger.info(f"去重完成，删除了 {self.stats['duplicates_removed']} 条重复记录")
            logger.info(f"剩余 {len(self.df)} 条唯一记录")
            
            return True
            
        except Exception as e:
            error_msg = f"去重处理失败: {str(e)}"
            logger.error(error_msg)
            self.stats['errors'].append(error_msg)
            return False
            
    def write_to_database(self, if_exists: str = 'append') -> bool:
        """
        将数据写入 PostgreSQL 数据库
        
        Args:
            if_exists: 表存在时的处理方式 ('fail', 'replace', 'append')
            
        Returns:
            写入成功返回 True，否则返回 False
        """
        try:
            if self.df is None or self.df.empty:
                logger.warning("没有数据需要写入数据库")
                return True
                
            if self.engine is None:
                error_msg = "数据库连接未建立"
                logger.error(error_msg)
                self.stats['errors'].append(error_msg)
                return False
                
            logger.info(f"开始将数据写入数据库表: {self.config['db']['table']}")
            
            write_df = self.df.copy()
            write_df['created_at'] = datetime.now()
            write_df['updated_at'] = datetime.now()
            
            columns_to_write = [
                'order_id', 'user_id', 'order_date', 'amount', 
                'status', 'product_name', 'quantity', 'created_at', 'updated_at'
            ]
            columns_to_write = [col for col in columns_to_write if col in write_df.columns]
            write_df = write_df[columns_to_write]
            
            write_df.to_sql(
                name=self.config['db']['table'],
                con=self.engine,
                if_exists=if_exists,
                index=False,
                chunksize=1000
            )
            
            self.stats['rows_written_to_db'] = len(write_df)
            logger.info(f"成功写入 {self.stats['rows_written_to_db']} 条记录到数据库")
            
            return True
            
        except SQLAlchemyError as e:
            error_msg = f"写入数据库失败: {str(e)}"
            logger.error(error_msg)
            self.stats['errors'].append(error_msg)
            return False
        except Exception as e:
            error_msg = f"数据写入过程中发生错误: {str(e)}"
            logger.error(error_msg)
            self.stats['errors'].append(error_msg)
            return False
            
    def generate_report(self) -> str:
        """
        生成处理摘要报告
        
        Returns:
            报告文本
        """
        self.stats['end_time'] = datetime.now()
        duration = (self.stats['end_time'] - self.stats['start_time']).total_seconds()
        
        report = f"""
{'='*80}
                    订单数据 ETL 处理摘要报告
{'='*80}

【基本信息】
处理开始时间: {self.stats['start_time'].strftime('%Y-%m-%d %H:%M:%S')}
处理结束时间: {self.stats['end_time'].strftime('%Y-%m-%d %H:%M:%S')}
总处理时长: {duration:.2f} 秒

【数据统计】
- 从 CSV 读取的总记录数: {self.stats['total_rows_read']:,}
- 数据清洗后剩余记录数: {self.stats['rows_after_cleaning']:,}
- 移除的重复记录数: {self.stats['duplicates_removed']:,}
- 最终写入数据库的记录数: {self.stats['rows_written_to_db']:,}

【数据质量分析】
数据清洗率: {(self.stats['rows_after_cleaning'] / self.stats['total_rows_read'] * 100) if self.stats['total_rows_read'] > 0 else 0:.2f}%
去重率: {(self.stats['duplicates_removed'] / self.stats['total_rows_read'] * 100) if self.stats['total_rows_read'] > 0 else 0:.2f}%
最终入库率: {(self.stats['rows_written_to_db'] / self.stats['total_rows_read'] * 100) if self.stats['total_rows_read'] > 0 else 0:.2f}%

【处理状态】
"""
        
        if self.stats['errors']:
            report += f"""
⚠️  处理过程中出现 {len(self.stats['errors'])} 个错误:
"""
            for i, error in enumerate(self.stats['errors'], 1):
                report += f"   {i}. {error}\n"
        else:
            report += """
✅  处理完成，未出现错误
"""
        
        if self.df is not None and not self.df.empty:
            report += f"""
【数据预览】
前 5 条记录:
{self.df.head().to_string()}

数据列信息:
"""
            for col, dtype in self.df.dtypes.items():
                non_null = self.df[col].count()
                report += f"   - {col}: {dtype}, 非空值: {non_null:,}\n"
                
            if 'amount' in self.df.columns:
                report += f"""
【金额统计】
总金额: ¥{self.df['amount'].sum():,.2f}
平均金额: ¥{self.df['amount'].mean():,.2f}
最大金额: ¥{self.df['amount'].max():,.2f}
最小金额: ¥{self.df['amount'].min():,.2f}
"""
                
            if 'status' in self.df.columns:
                report += f"""
【订单状态分布】
"""
                status_counts = self.df['status'].value_counts()
                for status, count in status_counts.items():
                    percentage = (count / len(self.df) * 100)
                    report += f"   - {status}: {count:,} ({percentage:.2f}%)\n"
                    
            if 'order_date' in self.df.columns:
                report += f"""
【日期范围】
最早订单日期: {self.df['order_date'].min().strftime('%Y-%m-%d %H:%M:%S')}
最晚订单日期: {self.df['order_date'].max().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        report += f"""
{'='*80}
                              报告结束
{'='*80}
"""
        return report
        
    def save_report(self, report: str, output_path: Optional[str] = None) -> str:
        """
        保存报告到文件
        
        Args:
            report: 报告文本
            output_path: 输出文件路径
            
        Returns:
            保存的文件路径
        """
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = f'etl_report_{timestamp}.txt'
            
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
            
        logger.info(f"报告已保存到: {output_path}")
        return output_path
        
    def run(self, csv_path: str, if_exists: str = 'append', 
            output_report: bool = True) -> Dict[str, Any]:
        """
        执行完整的 ETL 流程
        
        Args:
            csv_path: CSV 文件路径
            if_exists: 表存在时的处理方式
            output_report: 是否输出报告
            
        Returns:
            处理统计信息
        """
        self.stats['start_time'] = datetime.now()
        logger.info("="*80)
        logger.info("开始执行订单数据 ETL 流程")
        logger.info("="*80)
        
        try:
            if not self.read_csv(csv_path):
                logger.error("读取 CSV 文件失败，终止 ETL 流程")
                return self.stats
                
            if not self.clean_and_transform():
                logger.error("数据清洗失败，终止 ETL 流程")
                return self.stats
                
            if not self.remove_duplicates():
                logger.error("去重处理失败，终止 ETL 流程")
                return self.stats
                
            if self.engine is not None:
                self.create_table_if_not_exists()
                if not self.write_to_database(if_exists):
                    logger.warning("写入数据库失败，但将继续生成报告")
            else:
                logger.warning("数据库连接未建立，跳过数据库写入步骤")
                
            report = self.generate_report()
            
            if output_report:
                print(report)
                self.save_report(report)
                
            logger.info("="*80)
            logger.info("ETL 流程执行完成")
            logger.info("="*80)
            
        except Exception as e:
            error_msg = f"ETL 流程执行失败: {str(e)}"
            logger.error(error_msg)
            self.stats['errors'].append(error_msg)
            
        return self.stats


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='订单数据 ETL 处理脚本')
    parser.add_argument('csv_path', help='CSV 文件路径')
    parser.add_argument('--if-exists', choices=['fail', 'replace', 'append'], 
                        default='append', help='表存在时的处理方式')
    parser.add_argument('--no-db', action='store_true', help='跳过数据库写入')
    parser.add_argument('--no-report', action='store_true', help='不生成报告文件')
    
    args = parser.parse_args()
    
    etl = OrderETL()
    etl.load_config_from_env()
    
    if not args.no_db:
        if not etl.connect_to_database():
            logger.warning("数据库连接失败，将以仅文件模式运行")
            etl.engine = None
    
    stats = etl.run(
        csv_path=args.csv_path,
        if_exists=args.if_exists,
        output_report=not args.no_report
    )
    
    if stats['errors']:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()

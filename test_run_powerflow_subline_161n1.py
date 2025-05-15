import unittest
from unittest.mock import patch, MagicMock
from webinterface.src.run_powerflow_subline_161n1 import Run_Powerflow_of_subline

class TestRunPowerflowOfSubline(unittest.TestCase):

    @patch('webinterface.src.run_powerflow_subline_161n1.Run_Powerflow_of_subline')
    def test_run_powerflow_of_subline(self, mock_module):
        # 模擬Run_Powerflow_of_subline函數的依賴
        # 這裡需要根據實際函數的實現來模擬相應的依賴
        mock_module.return_value = MagicMock()

        # 測試正常的執行流程
        result = Run_Powerflow_of_subline(
            source_Folder='Data/User/AnonymousUser/SavFile/Powerflow',
            powerflow_folder='Data/User/AnonymousUser/SavFile/Powerflow',
            user='AnonymousUser',
            Sav_File=['122P.sav'],
            zone_num=[],
            area_num=[1],
            maxbasekv=161.0,
            minbasekv=161.0,
            confile_type='161KV_N-1'
        )

        # 根据实际函数的返回值进行断言
        # 這裡需要根據實際函數的行為來設置預期結果
        expected_result = {
            'error': 0,
            'return_value': [[{'content': 'PowerFlow-122P.sav  沒有分歧', 'errorcode': 0}]], 
            'which_log': 'Powerflow_Subline_Log'
            # 預期返回的字典內容
        }
        self.assertEqual(result, expected_result)

        # # 測試未找到 'X----------- FROM BUS ------------X X------------ TO BUS -------------X' 字串的情況
        # mock_module.return_value.find.side_effect = [-1, 100]  # 第一次查找返回-1
        # result = Run_Powerflow_of_subline(
        #     source_Folder='test_folder',
        #     powerflow_folder='test_powerflow_folder',
        #     user='test_user',
        #     Sav_File=['test_file1', 'test_file2'],
        #     zone_num=[1, 2, 3],
        #     area_num=[1, 2],
        #     maxbasekv=300,
        #     minbasekv=100,
        #     confile_type='test_type'
        # )
        # self.assertEqual(result, "未找到 'X----------- FROM BUS ------------X X------------ TO BUS -------------X' 字串")

        # # 測試未找到 'Output completed' 字串的情況
        # mock_module.return_value.find.side_effect = [100, -1]  # 第二次查找返回-1
        # result = Run_Powerflow_of_subline(
        #     source_Folder='test_folder',
        #     powerflow_folder='test_powerflow_folder',
        #     user='test_user',
        #     Sav_File=['test_file1', 'test_file2'],
        #     zone_num=[1, 2, 3],
        #     area_num=[1, 2],
        #     maxbasekv=300,
        #     minbasekv=100,
        #     confile_type='test_type'
        # )
        # self.assertEqual(result, "未找到 'Output completed' 字串")

if __name__ == '__main__':
    # unittest.main()
    result = Run_Powerflow_of_subline(
        source_Folder='../Data/User/AnonymousUser/SavFile/Powerflow',
        powerflow_folder='../Data/User/AnonymousUser/SavFile/Powerflow',
        user='AnonymousUser',
        Sav_File=['122P.sav'],
        zone_num=[],
        area_num=['1'],
        maxbasekv=161.0,
        minbasekv=161.0,
        confile_type='161KV_N-1'
    )
    print(result)
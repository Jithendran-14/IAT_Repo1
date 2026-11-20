import unittest
from workshop.common import load_config,check_chunk_settings,sources,safe_table,verify_rows

class ChallengeConfig(unittest.TestCase):
    def test_valid_chunking_parameters(self):
        check_chunk_settings(load_config())
    def test_supported_documents_present(self):
        self.assertTrue(sources(load_config()))

class VerificationControls(unittest.TestCase):
    def test_empty_output_cannot_pass(self):
        with self.assertRaises(ValueError):verify_rows([], 'source')
    def test_wrong_vector_dimension_cannot_pass(self):
        with self.assertRaises(ValueError):verify_rows([('source',3,{'chunk_id':'x'})],'source')
    def test_missing_metadata_cannot_pass(self):
        with self.assertRaises(ValueError):verify_rows([('source',1024,{})],'source')
    def test_partial_content_cannot_pass(self):
        with self.assertRaises(ValueError):verify_rows([('one',1024,{'chunk_id':'x'})],'one two')
    def test_valid_rows_pass(self):
        result=verify_rows([('one two',1024,{'chunk_id':'x'})],'one two')
        self.assertEqual(result['persisted_chunks'],1)
    def test_original_table_cannot_be_targeted(self):
        with self.assertRaises(ValueError):safe_table('LOCAL_RAG_EMBEDDINGS')
    def test_injected_identifier_cannot_be_targeted(self):
        with self.assertRaises(ValueError):safe_table('IAT_R1_E_ABC; DROP TABLE x')
    def test_generated_table_allowed(self):
        self.assertEqual(safe_table('IAT_R1_E_012345ABCDEF'),'IAT_R1_E_012345ABCDEF')

if __name__=='__main__':unittest.main()

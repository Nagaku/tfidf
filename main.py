# alur dari sini trus ke errors, document
from document import docs, doc_init, write_output

def main():
    doc_init()
    
    for doc in docs:
        print(doc.tf_idf.frekuensi_term)
        print()
        # print(doc.tf_idf.tf_val)
        # print()
        # print(doc.tf_idf.idf_val)
        # print()
        # print(doc.tf_idf.tf_idf_val)
        # print()

if __name__ == "__main__":
    main()
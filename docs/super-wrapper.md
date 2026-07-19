# SuperWrapper

The `SuperWrapper` is a utility class that provides a method wrapping mechanism, allowing parent class methods to be executed before and after child class methods. It's like an inversion of the traditional `super()` call pattern.

## Overview

In traditional inheritance, a child class can call its parent's method using `super()`. SuperWrapper flips this around: the parent class method calls the child class method. This creates a nested execution pattern where each parent in the inheritance chain can perform actions before and after the child's method runs.

## How It Works

SuperWrapper provides a decorator (`@ParentClass.wrap`) that wraps a method so that it's called within the inherited version of that method. This creates a chain of method calls that execute from the top of the inheritance hierarchy down to the most specific implementation, and then back up again.

## Key Differences from Traditional Inheritance

1. **Execution Order**: In traditional inheritance with `super()`, execution flows from child to parent. With SuperWrapper, execution flows from parent to child and back to parent.

2. **Method Signatures**: In SuperWrapper, parent methods have a different signature than child methods. Parent methods receive the child method as their first argument, followed by any arguments passed to the child method.

3. **Explicit Method Calling**: Parent methods must explicitly call the child method that's passed to them.

## Example: Document Processing System

Imagine you're building a document processing system that handles various types of documents (legal contracts, financial reports, technical specifications). Each document type needs specific processing, but all documents share common steps like validation, formatting, and archiving.

```python
from wizlib.super_wrapper import SuperWrapper

class DocumentProcessor(SuperWrapper):
    """Base document processor with common steps for all documents"""
    
    def process(self, method, document, **options):
        """Process any document with common steps before and after"""
        print(f"Starting processing of document: {document['title']}")
        
        # Common pre-processing steps
        self.validate_metadata(document)
        self.backup_original(document)
        
        # Execute the specific document type's processing
        result = method(self, document, **options)
        
        # Common post-processing steps
        self.format_output(result)
        self.archive_document(document, result)
        
        print(f"Completed processing of document: {document['title']}")
        return result
    
    def validate_metadata(self, document):
        """Ensure document has required metadata"""
        required_fields = ['title', 'author', 'date']
        for field in required_fields:
            if field not in document:
                raise ValueError(f"Document missing required field: {field}")
    
    def backup_original(self, document):
        """Create a backup of the original document"""
        print(f"Creating backup of original document")
    
    def format_output(self, result):
        """Apply standard formatting to the output"""
        print(f"Applying standard formatting to output")
    
    def archive_document(self, document, result):
        """Archive the document and its processed result"""
        print(f"Archiving document and processing results")


class LegalDocumentProcessor(DocumentProcessor):
    """Processor for legal documents with additional compliance checks"""
    
    @DocumentProcessor.wrap
    def process(self, method, document, **options):
        """Add legal-specific processing steps"""
        print(f"Performing legal compliance check")
        
        # Legal-specific pre-processing
        self.check_legal_compliance(document)
        
        # Execute the specific legal document type's processing
        result = method(self, document, **options)
        
        # Legal-specific post-processing
        self.add_legal_disclaimer(result)
        
        print(f"Legal processing completed")
        return result
    
    def check_legal_compliance(self, document):
        """Check document for legal compliance issues"""
        print(f"Checking document for legal compliance")
    
    def add_legal_disclaimer(self, result):
        """Add legal disclaimers to the processed document"""
        print(f"Adding legal disclaimers to output")


class ContractProcessor(LegalDocumentProcessor):
    """Processor specifically for contract documents"""
    
    @LegalDocumentProcessor.wrap
    def process(self, document, **options):
        """Process a contract document"""
        print(f"Processing contract-specific elements")
        
        # Extract contract terms
        terms = self.extract_contract_terms(document)
        
        # Analyze contract risks
        risks = self.analyze_contract_risks(terms)
        
        # Generate contract summary
        summary = {
            'document': document['title'],
            'terms': terms,
            'risks': risks,
            'recommendation': 'Approve' if not risks else 'Review'
        }
        
        print(f"Contract processing completed with recommendation: {summary['recommendation']}")
        return summary
    
    def extract_contract_terms(self, document):
        """Extract key terms from the contract"""
        print(f"Extracting key terms from contract")
        return ['Term 1', 'Term 2', 'Term 3']
    
    def analyze_contract_risks(self, terms):
        """Analyze contract terms for potential risks"""
        print(f"Analyzing contract terms for risks")
        return []


# Example usage
contract = {
    'title': 'Service Agreement',
    'author': 'Legal Department',
    'date': '2023-03-15',
    'content': 'This agreement is made between...'
}

processor = ContractProcessor()
result = processor.process(contract, validate_signatures=True)
print(f"\nFinal result: {result}")
```

Output:
```
Starting processing of document: Service Agreement
Performing legal compliance check
Checking document for legal compliance
Processing contract-specific elements
Extracting key terms from contract
Analyzing contract terms for risks
Contract processing completed with recommendation: Approve
Adding legal disclaimers to output
Legal processing completed
Applying standard formatting to output
Archiving document and processing results
Completed processing of document: Service Agreement

Final result: {'document': 'Service Agreement', 'terms': ['Term 1', 'Term 2', 'Term 3'], 'risks': [], 'recommendation': 'Approve'}
```

## Use Cases

SuperWrapper is particularly useful for:

1. **Setup and Teardown**: Performing setup actions before a method runs and cleanup actions afterward
2. **Logging and Monitoring**: Adding logging or monitoring around method execution
3. **Transaction Management**: Starting and committing/rolling back transactions
4. **Resource Management**: Acquiring and releasing resources
5. **Validation**: Validating inputs before execution and outputs after execution

## Implementation Requirements

For a method to be "wrappable" with SuperWrapper:

1. The parent class method must accept a `method` parameter as its first argument (after `self`)
2. The parent class method must explicitly call the passed method: `method(self, *args, **kwargs)`
3. The child class method must use the `@ParentClass.wrap` decorator

Note that this is different from regular inheritance, where the parent class method has the same signature as the child class method.

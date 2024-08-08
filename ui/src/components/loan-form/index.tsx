import React, { useState } from 'react';
import axios from 'axios';
import convertCamelToSnakeCase from '../../utils/helpers';

interface LoanFormProps {
  onLoanSubmit: (loanData: any) => void;
}

const LoanForm: React.FC<LoanFormProps> = ({ onLoanSubmit }) => {
  const [loanDetails, setLoanDetails] = useState({
    loanAmount: '',
    interestRate: '',
    loanTerm: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setLoanDetails({ ...loanDetails, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const formData = convertCamelToSnakeCase(loanDetails);
      const response = await axios.post('http://localhost:8000/loans/loanoffers/', formData);
      onLoanSubmit(response.data);
    } catch (error) {
      console.error('Error submitting loan details:', error);
    }
  };

  return (
    <form className="flex-row" onSubmit={handleSubmit}>
      <input
        type="number"
        name="loanAmount"
        value={loanDetails.loanAmount}
        onChange={handleChange}
        placeholder="Loan Amount"
        required
      />
      <input
        type="number"
        name="interestRate"
        value={loanDetails.interestRate}
        onChange={handleChange}
        placeholder="Interest Rate (%)"
        required
      />
      <input
        type="number"
        name="loanTerm"
        value={loanDetails.loanTerm}
        onChange={handleChange}
        placeholder="Loan Term (months)"
        required
      />
      <button type="submit">Submit</button>
    </form>
  );
};

export default LoanForm;

/**
 * Simple script to test if the backend is accessible
 */
const { exec } = require('child_process');

console.log('Testing backend connection...');
console.log('Expected backend URL: http://localhost:8000/health');

// Test if backend is running by checking the health endpoint
async function testBackendConnection() {
  try {
    const response = await fetch('http://localhost:8000/health');
    if (response.ok) {
      const data = await response.json();
      console.log('✅ Backend is running and accessible!');
      console.log('Health check response:', data);
      return true;
    } else {
      console.log('❌ Backend returned error:', response.status, response.statusText);
      return false;
    }
  } catch (error) {
    console.log('❌ Backend is not accessible. Error:', error.message);
    console.log('\n💡 Hint: Make sure to start the backend server first:');
    console.log('   python run_backend.py');
    return false;
  }
}

// For Node.js environments without fetch (older versions)
function testWithCurlOrPython() {
  console.log('\nTesting with alternative method...');

  // Test using curl or python if fetch is not available
  const testCommand = process.platform === 'win32'
    ? 'curl -s -o nul -w "%{http_code}" http://localhost:8000/health 2>nul || python -c "import urllib.request; print(urllib.request.urlopen(\'http://localhost:8000/health\').getcode())" 2>nul || echo "Cannot connect"'
    : 'curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health || echo "Cannot connect"';

  exec(testCommand, (error, stdout, stderr) => {
    if (stdout && !stdout.includes('Cannot connect')) {
      console.log('✅ Backend appears to be running (response code:', stdout.trim(), ')');
    } else {
      console.log('❌ Backend is not accessible');
      console.log('\n💡 Hint: Make sure to start the backend server first:');
      console.log('   python run_backend.py');
    }
  });
}

// Run the test
if (typeof fetch !== 'undefined') {
  testBackendConnection();
} else {
  testWithCurlOrPython();
}

console.log('\n📝 To run the full application:');
console.log('1. Terminal 1: python run_backend.py');
console.log('2. Terminal 2: cd frontend && npm run dev');